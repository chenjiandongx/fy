#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    author="chenjiandongx",
    author_email="chenjiandongx@qq.com",
    name="fy",
    version="1.0.0",
    license="MIT",
    url="https://github.com/chenjiandongx/fy",
    py_modules=["fy"],
    install_requires=["requests", "huepy"],
    description="Translate words via command line",
    entry_points={"console_scripts": ["fy=fy:command_line_runner"]},
)
