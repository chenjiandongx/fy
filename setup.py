#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

# RELEASE STEPS
# $ python setup.py sdist
# $ twine upload dist/VX.Y.Z.tar.gz
# $ git tag -a VX.Y.Z -m "release version VX.Y.Z"
# $ git push origin VX.Y.Z

setup(
    author="chenjiandongx",
    author_email="chenjiandongx@qq.com",
    name="fy",
    version="1.2.0",
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
