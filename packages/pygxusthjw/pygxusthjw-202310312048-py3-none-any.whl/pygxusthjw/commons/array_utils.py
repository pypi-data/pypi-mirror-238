#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        array_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为类似“数组”的对象提供辅助函数和类。
#                   Outer Parameters: xxxxxxx
# Class List:       Ordering -- 枚举`Ordering`表征有序性。
# Function List:    hash_code(*args) -- 计算可变参数组的hash码。
#                   is_sorted(arr: npt.ArrayLike) --
#                                              判断指定的值组是否为有序的。
#                   is_sorted_ascending(arr: npt.ArrayLike) --
#                                              判断指定的值组是否为升序的。
#                   is_sorted_descending(arr: npt.ArrayLike) --
#                                              判断指定的值组是否为降序的。
#                   reverse(arr: npt.ArrayLike) -- 将指定的值组倒置。
#                   is_equals_of(arr1: npt.ArrayLike,
#                                arr2: npt.ArrayLike,
#                                rtol=0, atol=1e-9) --
#                                                   判断两个数组的相等性。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import numpy as np
import numpy.typing as npt

from enum import Enum


# ==================================================================
def hash_code(*args) -> int:
    """
    计算可变参数组的hash码。

    参考自：`java.util.Arrays.hashCode(Object ...args)`方法的算法。

    :param args: 可变参数组。
    :return: hash码。
    :rtype: `int`
    """
    if args is None:
        return 0

    result: int = 1
    for arg in args:
        result = 31 * result + (0 if arg is None else hash(arg))

    return result


def is_sorted(arr: npt.ArrayLike) -> bool:
    """
    判断指定的值组是否为有序的，
    如果是有序的（无论升序或降序），返回True，
    否则返回False。

    :param arr: 指定的值组。
    :return:如果指定的值组是有序的（无论升序或降序），
    返回True，否则返回False。
    """
    value_arr = np.array(arr, copy=False)
    return np.all(np.diff(value_arr) >= 0) or \
        np.all(np.diff(value_arr) <= 0)


def is_sorted_ascending(arr: npt.ArrayLike) -> bool:
    """
    判断指定的值组是否为升序的，
    如果是升序的，返回True，
    否则返回False。

    :param arr: 指定的值组。
    :return:如果指定的值组是升序的，
    返回True，否则返回False。
    """
    value_arr = np.array(arr, copy=False)
    return np.all(np.diff(value_arr) >= 0)


def is_sorted_descending(arr: npt.ArrayLike) -> bool:
    """
    判断指定的值组是否为降序的，
    如果是降序的，返回True，
    否则返回False。

    :param arr: 指定的值组。
    :return:如果指定的值组是降序的，
    返回True，否则返回False。
    """
    value_arr = np.array(arr, copy=False)
    return np.all(np.diff(value_arr) <= 0)


def reverse(arr: npt.ArrayLike) -> npt.NDArray:
    """
    将指定的值组倒置。

    :param arr: 指定的值组。
    :return: 倒置后的值组。
    """
    value_arr = np.array(arr, copy=False)
    return np.array(value_arr[::-1], copy=True)


def is_equals_of(arr1: npt.ArrayLike,
                 arr2: npt.ArrayLike,
                 rtol=0, atol=1e-9):
    """
    判断两个数组的相等性。

    第1个参数记为：a

    第2个参数记为：b

    则下式为True，此函数返回True：

        absolute(a - b) <= (atol + rtol * absolute(b))

    :param arr1: 数组1。
    :param arr2: 数组2。
    :param rtol: 相对容差，相对容差是指：两个数之差除以第2个数。
    :param atol: 绝对容差，绝对容差是指：两个数之差。
    :return:相等则返回True，否则返回false。
    """
    return np.allclose(np.array(arr1, copy=False),
                       np.array(arr2, copy=False),
                       rtol=rtol, atol=atol,
                       equal_nan=True)


class Ordering(Enum):
    """
    枚举`Ordering`表征有序性。
    """
    # 无序。
    unordered = 0
    """
    ‘unordered’表征无序。
    """

    # 升序。
    ascending = 1
    """
    ‘ascending’表征升序。
    """

    # 降序。
    descending = 2
    """
    ‘descending’表征降序。
    """
