#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        object_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为‘对象’提供一些可共用的方法。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    gen_hash(*args) -- 生成可变参数组的hash码。
#                   safe_repr(obj: object, short: bool = False,
#                             max_length: int = 80) --
#                             获取指定对象的__repr__信息值。
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
# ------------------------------------------------------------------
# 导包 =============================================================
from .array_utils import hash_code


# ==================================================================
def gen_hash(*args) -> int:
    """
    生成可变参数组的hash码。

    :param args: 可变参数组。
    :return: hash码。
    :rtype: `int`
    """
    return hash_code(*args)


def safe_repr(obj: object, short: bool = False,
              max_length: int = 80) -> str:
    """
    获取指定对象的__repr__信息值。

    :param obj: 指定的对象。
    :param short: 是否简短信息，True表示简短信息，False表示不简短信息。
    :param max_length: 若简短信息，则此值指定允许信息的最大长度。
    :return: 对象的__repr__信息值。
    """
    # noinspection PyBroadException
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < max_length:
        return result
    return result[:max_length] + ' [truncated]...'
