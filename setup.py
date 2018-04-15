#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    author="chenjiandongx",
    author_email="chenjiandongx@qq.com",
    name="youdao-wd",
    version="0.1.0",
    license="MIT",
    url="https://github.com/chenjiandongx/youdao-wd",
    py_modules=["youdao"],
    description="Query words meanings via the command line",
    entry_points={"console_scripts": ["wd=youdao:command_line_runner"]},
)
