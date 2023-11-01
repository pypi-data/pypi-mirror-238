# taskbeat

In memory task schedule support cron tasks, interval tasks and onetime tasks. Using python's asyncio.

## Install

```
pip install taskbeat
```

## Important

More than 1,000,000 60-SECOND-CYCLE tasks may cuase task delay sometimes. The limit is depends on your CPU mostly, you'd better to test to find the limitation on you server before you use it in production.

## Python Compatibility

- Compatible with python3.7 and above.
- Tested with python3.7, python3.8, python3.9, python3.10, python3.11 and python3.12.

## Example 1

```python
import time
import logging
import asyncio

from taskbeat import TaskBeat

_logger = logging.getLogger(__name__)


async def report(beat):
    """It should be showing report every second.

    If it is not showing report every second,
    then your tasks mostly are not fired on time.
    """
    last_counter = 0
    while True:
        delta = beat.event_counter - last_counter
        last_counter = beat.event_counter
        with open("stats.txt", "a", encoding="utf-8") as fobj:
            fobj.write(str(time.time()) + " " + str(delta) + "\n")
        await asyncio.sleep(1)


async def beat_server():
    beat = TaskBeat()
    task = asyncio.create_task(report(beat))
    for i in range(800 * 1000):
        event_id = "cron_{}".format(i)
        await beat.update_cron_task(event_id, "* * * * *")
    while True:
        event_id = await beat.get_event(5)
        if event_id == "cron_1":
            # should be showing every minute
            # see how many seconds a task may daley here
            _logger.info("cron_1=%s", time.time())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(beat_server())
```

## Releases

### v0.1.0

- First release.

### v0.1.1

- Fix delete_task problem.
