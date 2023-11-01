#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        numpy_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为"numpy"包提供一些附加的方法。
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
import numpy as np
import numpy.typing as npt
from .math_plus import math_round


# ==================================================================
def numpy_round(x):
    """
    计算一个值四舍五入后的结果。

    Python系统提供有round函数，但此函数存在一个问题，即:
    round(0.5)  ---> 0

    此函数可以避开Python内置round函数的问题。

    :param x: 需要计算的值。
    :return: 四舍五入后的值。
    """
    res = np.empty_like(x)
    for i in range(len(x)):
        res[i] = math_round(x[i])
    return res


def numpy_sech(x, *args, **kwargs):
    """
    基于numpy.cosh函数（双曲余弦），针对参数x的元素计算其双曲正割。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲正割
    """
    return 1.0 / np.cosh(x, *args, **kwargs)


def sech(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲正割。

    :param x: array_like，Input array.
    :return: 双曲正割
    """
    return 2.0 / (np.exp(x) + np.exp(-x))


def numpy_coth(x, *args, **kwargs):
    """
    基于numpy.tanh函数（双曲正切），针对参数x的元素计算其双曲余切。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲余切
    """
    return 1.0 / np.tanh(x, *args, **kwargs)


def coth(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲余切。

    :param x: array_like，Input array.
    :return: 双曲余切
    """
    return (np.exp(x) + np.exp(-x)) / (np.exp(x) - np.exp(-x))


def numpy_cech(x, *args, **kwargs):
    """
    基于numpy.sinh函数（双曲正弦），针对参数x的元素计算其双曲余割。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲余割。
    """
    return 1.0 / np.sinh(x, *args, **kwargs)


def cech(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲余割。

    :param x: array_like，Input array.
    :return: 双曲余割。
    """
    return 2.0 / (np.exp(x) - np.exp(-x))
