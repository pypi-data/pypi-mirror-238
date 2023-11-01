#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        math_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为"math"包提供一些附加的方法。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import math


# ==================================================================

def math_round(value):
    """
    计算一个值四舍五入后的结果。

    Python系统提供有round函数，但此函数存在一个问题，即:
    round(0.5)  ---> 0

    此函数可以避开Python内置round函数的问题。

    :param value: 需要计算的值。
    :return: 四舍五入后的值。
    """
    res = math.floor(value)
    fraction = value - res
    if fraction >= 0.5:
        res = math.ceil(value)
    return res
