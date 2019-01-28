#!/usr/bin/env python
# coding=utf-8

from setuptools import find_packages, setup

# RELEASE STEPS
# $ python setup.py sdist
# $ twine upload dist/VX.Y.Z.tar.gz
# $ git tag -a VX.Y.Z -m "release version VX.Y.Z"
# $ git push origin VX.Y.Z

setup(
    author="chenjiandongx",
    author_email="chenjiandongx@qq.com",
    name="fy",
    version="1.4.1",
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
        "litecli",
        "pony",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    description="Translate words via command line",
    entry_points={"console_scripts": ["fy=fy:command_line_runner"]},
)
