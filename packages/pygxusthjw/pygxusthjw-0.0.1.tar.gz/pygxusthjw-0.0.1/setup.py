#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        setup.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: pygxusthjw包的setup.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/24     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from setuptools import setup, find_packages

# 定义 ============================================================


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="pygxusthjw",
    version="0.0.1",
    author="gxusthjw",
    author_email="jiweihuang@vip.163.com",
    description="the python libraries of gxusthjw.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://codeup.aliyun.com/64eb4482dba61e96ebf630f1/Python/gxusthjw-pypackages/tree/master/pygxusthjw",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",

        "statsmodels",

        "lmfit",

        "pyampd",
        "ampdLib",

        "findiff",
        "numdifftools",

        "pybaselines",

        "pytest",

        "chardet",

    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
