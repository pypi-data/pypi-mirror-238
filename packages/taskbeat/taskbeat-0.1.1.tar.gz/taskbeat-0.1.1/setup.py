#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = []
with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires += [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="taskbeat",
    version="0.1.1",
    description="In memory task schedule support cron tasks, interval tasks and onetime tasks. Using python's asyncio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    author="Chen Jia",
    author_email="chenjia@zencore.cn",
    maintainer="Chen Jia",
    maintainer_email="chenjia@zencore.cn",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["taskbeat"],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["taskbeat"],
    zip_safe=False,
    include_package_data=True,
)
