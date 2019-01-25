#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    author="chenjiandongx",
    author_email="chenjiandongx@qq.com",
    name="fy",
    version="1.1.0",
    license="MIT",
    url="https://github.com/chenjiandongx/fy",
    py_modules=["fy"],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "requests",
        "huepy",
        "xmltodict",
        "pywin32;sys_platform=='win32'",
        "prompt_toolkit>=2.0.7",
    ],
    description="Translate words via command line",
    entry_points={"console_scripts": ["fy=fy:command_line_runner"]},
)
