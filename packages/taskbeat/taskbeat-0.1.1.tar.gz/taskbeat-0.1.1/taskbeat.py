import time
import heapq
import random
import logging
import asyncio

import croniter

_logger = logging.getLogger(__name__)

CRON = "cron"
INTERVAL = "interval"
ONETIME = "onetime"
TASK_ADDED = 1
TASK_UPDATED = 2
TASK_NOT_CHANGED = 3


class UnknownRuleType(ValueError):
    def __init__(self, rule_type):
        super().__init__("unknown rule type", rule_type)


class Rule(object):
    """任务规则生成器。

    next函数，提示下一次事件时间戳。
    next函数返回为None时，表示不再有后续事件生成。
    """


class CronIter(Rule):
    def __init__(self, rule, random_delay):
        self.rule = rule
        self.random_delay = random_delay
        self.iter_delay = random.randint(0, self.random_delay)
        self.inter = croniter.croniter(rule)

    def next(self):
        return self.inter.next() + self.iter_delay


class IntervalIter(Rule):
    def __init__(self, interval, random_delay):
        self.stime = time.time()
        self.interval = interval
        self.random_delay = random_delay
        self.iter_delay = random.randint(0, self.random_delay)
        self.next_time = self.stime + self.iter_delay

    def next(self):
        self.next_time += self.interval
        return self.next_time


class OnetimeIter(Rule):
    def __init__(self, time):
        self.time = time
        self.next_time = self.time

    def next(self):
        time = self.next_time
        self.next_time = None
        return time


class TaskBeat(object):
    """任务调度器。

    根据任务规则，产生事件，插入到事件队列中。
    支撑的任务规则有：
    - cron规则
    - interval规则
    - onetime规则
    """

    DEFAULT_EMERGENCY_SECONDS = 3600

    def __init__(self, emergency_seconds=None):
        self.emergency_seconds = emergency_seconds or self.DEFAULT_EMERGENCY_SECONDS
        # 统计数据初始化
        self.event_counter = 0
        self.event_counters = {}
        self.event_queue = asyncio.Queue()
        # 任务数据初始化
        self.tasks = {}
        self.emergency_tasks_stime = int(time.time())
        self.emergency_tasks_ioffset = 0
        self.non_emergency_tasks = []
        self.emergency_tasks = []
        for _ in range(self.emergency_seconds):
            self.emergency_tasks.append([])
        # 服务退出状态
        self._stop_flag = False
        self._stop_event = asyncio.Event()
        # 启动非紧急任务管理器
        self._task_beat_process_to_check_non_emergency_events = asyncio.create_task(
            self.task_beat_process_to_check_non_emergency_events()
        )
        # 启动紧急任务管理器
        self._task_beat_process_to_fire_emergency_events = asyncio.create_task(
            self.task_beat_process_to_fire_emergency_events()
        )

    async def add_event(self, event_id, time):
        """在内存中生成一个任务。等待被触发。"""
        delta = int(time) - self.emergency_tasks_stime
        if delta >= self.emergency_seconds:
            heapq.heappush(self.non_emergency_tasks, (time, event_id))
        else:
            index = (delta + self.emergency_tasks_ioffset) % self.emergency_seconds
            self.emergency_tasks[index].append(event_id)

    async def make_task_iter(self, rule_type, rule_args, rule_kwargs):
        if rule_type == CRON:
            return CronIter(*rule_args, **rule_kwargs)
        if rule_type == INTERVAL:
            return IntervalIter(*rule_args, **rule_kwargs)
        if rule_type == ONETIME:
            return OnetimeIter(*rule_args, **rule_kwargs)
        raise UnknownRuleType(rule_type)

    async def update_cron_task(self, event_id, rule, random_delay=None):
        if random_delay is None:
            random_delay = 60
        return await self.update_task(
            event_id,
            CRON,
            rule,
            random_delay=random_delay,
        )

    async def update_interval_task(self, event_id, interval, random_delay=None):
        if random_delay is None:
            random_delay = interval
        return await self.update_task(
            event_id,
            INTERVAL,
            interval,
            random_delay=random_delay,
        )

    async def update_onetime_task(self, event_id, time):
        return await self.update_task(
            event_id,
            ONETIME,
            time,
        )

    async def update_task(self, event_id, rule_type, *rule_args, **rule_kwargs):
        """创建新的任务，或更新任务设置，并启动任务调度器。

        @Returns:
            ${TASK_ADDED}=1: task added
            ${TASK_UPDATED}=2: task updated.
            ${TASK_NOT_CHANGED}=3: task no changes.
        """
        return_flag = None
        if not event_id in self.tasks:
            return_flag = TASK_ADDED
            _logger.debug(
                "add a new task: event_id=%s, rule_type=%s, rule_args=%s, rule_kwargs=%s",
                event_id,
                rule_type,
                rule_args,
                rule_kwargs,
            )
        else:
            # 比较新旧任务配置，如果任务设置没有变化，则不需要进行设置。
            task = self.tasks[event_id]
            is_same_flag = True
            if is_same_flag and rule_type != task["rule_type"]:
                is_same_flag = False
            if is_same_flag and rule_args != task["rule_args"]:
                is_same_flag = False
            if is_same_flag and rule_kwargs != task["rule_kwargs"]:
                is_same_flag = False
            if is_same_flag:
                return TASK_NOT_CHANGED
            else:
                return_flag = TASK_UPDATED
            _logger.debug(
                "update a running task: event_id=%s, old_rule_type=%s, old_rule_args=%s, old_rule_kwargs=%s, new_rule_type=%s, new_rule_args=%s, new_rule_kwargs",
                event_id,
                task["rule_type"],
                task["rule_args"],
                task["rule_kwargs"],
                rule_type,
                rule_args,
                rule_kwargs,
            )
            await self.delete_task(event_id)
        # add or update
        iter = await self.make_task_iter(rule_type, rule_args, rule_kwargs)
        self.event_counters[event_id] = 0
        self.tasks[event_id] = {
            "iter": iter,
            "next": iter.next(),
            "rule_type": rule_type,
            "rule_args": rule_args,
            "rule_kwargs": rule_kwargs,
        }
        await self.add_event(event_id, self.tasks[event_id]["next"])
        # return the flag
        return return_flag

    async def delete_task(self, event_id):
        """删除任务。"""
        _logger.debug(
            "delete task: event_id=%s",
            event_id,
        )
        if event_id in self.tasks:
            del self.tasks[event_id]
        is_schedule_deleted = False
        # 只有一个事件安排
        for index in range(self.emergency_seconds):
            try:
                self.emergency_tasks[index].remove(event_id)
                is_schedule_deleted = True
                break
            except ValueError:
                pass
        # 只有一个事件安排
        if not is_schedule_deleted:
            for index in range(len(self.non_emergency_tasks)):
                if self.non_emergency_tasks[index][1] == event_id:
                    del self.non_emergency_tasks[index]
                    is_schedule_deleted = True
                    break
        return is_schedule_deleted

    async def stop(self):
        """删除所有任务。"""
        _logger.info("TaskBeat stopping...")
        self._stop_flag = True
        self._stop_event.set()
        await self._task_beat_process_to_check_non_emergency_events
        await self._task_beat_process_to_fire_emergency_events
        self.tasks = {}
        self.non_emergency_tasks = []
        for _ in range(self.emergency_seconds):
            self.emergency_tasks.clear()
        _logger.info("TaskBeat stopped.")

    async def fire_event(self, event_id):
        """触发事件。并根据任务设置，添加下一个事件。"""
        self.event_counter += 1
        self.event_counters[event_id] += 1
        await self.event_queue.put(event_id)
        self.tasks[event_id]["next"] = self.tasks[event_id]["iter"].next()
        if self.tasks[event_id]["next"]:
            await self.add_event(event_id, self.tasks[event_id]["next"])

    async def get_event(self, timeout=None):
        if timeout is None:
            return await self.event_queue.get()
        else:
            try:
                return await asyncio.wait_for(self.event_queue.get(), timeout=timeout)
            except asyncio.TimeoutError:
                return None

    async def check_non_emergency_tasks(self):
        """检查非紧急事件列表。将达到紧急标准的事件移到相应的事件表中。"""
        check_index = 0
        non_emergency_tasks_size = len(self.non_emergency_tasks)
        while check_index < non_emergency_tasks_size:
            delta = (
                int(self.non_emergency_tasks[check_index][0])
                - self.emergency_tasks_stime
            )
            if delta < self.emergency_seconds:
                index = (delta + self.emergency_tasks_ioffset) % self.emergency_seconds
                self.emergency_tasks[index].append(
                    self.non_emergency_tasks[check_index][1]
                )
                check_index += 1
            else:
                break
        if check_index:
            self.non_emergency_tasks = self.non_emergency_tasks[check_index:]

    async def task_beat_process_to_check_non_emergency_events(self):
        _logger.info("task_beat_process_to_check_non_emergency_events start...")
        sleeptime = self.emergency_seconds / 10
        if sleeptime < 1:
            sleeptime = 1
        while not self._stop_flag:
            await self.check_non_emergency_tasks()
            try:
                await asyncio.wait_for(self._stop_event.wait(), sleeptime)
                break
            except asyncio.TimeoutError:
                pass
        _logger.info("task_beat_process_to_check_non_emergency_events end.")

    async def fire_emergency_events(self):
        """触发当前时间戳下所有事件。触发后：
        1、清空事件列表
        2、事件表指针偏移量加1
        3、当前时间戳加1
        """
        index = self.emergency_tasks_ioffset % self.emergency_seconds
        for event_id in self.emergency_tasks[index]:
            await self.fire_event(event_id)
        self.emergency_tasks[self.emergency_tasks_ioffset].clear()
        self.emergency_tasks_ioffset += 1
        self.emergency_tasks_stime += 1

    async def task_beat_process_to_fire_emergency_events(self):
        """任务调度器。"""
        _logger.info("task_beat_process_to_fire_emergency_events start...")
        while not self._stop_flag:
            if time.time() >= self.emergency_tasks_stime:
                await self.fire_emergency_events()
            sleeptime = self.emergency_tasks_stime - time.time()
            if sleeptime < 0:
                sleeptime = 0.01
            if sleeptime > 1:
                sleeptime = 0.99
            await asyncio.sleep(sleeptime)
        _logger.info("task_beat_process_to_fire_emergency_events end.")
