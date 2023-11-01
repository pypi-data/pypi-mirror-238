#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: pygxusthjw包的__init__.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .commons import (Base, Author, Version, Copyright,
                      hash_code, is_sorted, is_sorted_ascending,
                      is_sorted_descending, reverse, Ordering,
                      is_equals_of, gen_hash, safe_repr,
                      join_file_path, sep_file_path, math_round,
                      numpy_round, numpy_sech, numpy_cech,
                      numpy_coth, sech, cech, coth,
                      NUMERICAL_PRECISION, float_epsilon,
                      ARITHMETIC_PRECISION, TINY_FLOAT,
                      FLOAT_EPSILON, BOLTZMANN_CONSTANT,
                      GAS_CONSTANT, AVOGADRO_CONSTANT, IntervalRule,
                      Interval, StatisticalInterval, IntervalGroup,
                      FileInfo, get_file_encoding_chardet,
                      file_info, get_file_info, get_file_info_of_module,
                      DataTable, read_txt
                      )

# 定义 ============================================================
__version__ = "0.0.1"

__doc__ = """
the python libraries of gxusthjw.
"""

# noinspection DuplicatedCode
__all__ = [
    'Base', 'Author', 'Version', 'Copyright',
    'hash_code', 'is_sorted', 'is_sorted_ascending', 'is_sorted_descending',
    'reverse', 'Ordering', 'is_equals_of', 'gen_hash', 'safe_repr',
    'join_file_path', 'sep_file_path', 'math_round', 'numpy_round',
    'numpy_sech', 'numpy_cech', 'numpy_coth', 'sech', 'cech', 'coth',
    'NUMERICAL_PRECISION', 'ARITHMETIC_PRECISION', 'TINY_FLOAT',
    'FLOAT_EPSILON', 'float_epsilon', 'BOLTZMANN_CONSTANT',
    'GAS_CONSTANT', 'AVOGADRO_CONSTANT', 'IntervalRule', 'Interval',
    'StatisticalInterval', 'IntervalGroup', 'FileInfo',
    'get_file_encoding_chardet', 'file_info', 'get_file_info',
    'get_file_info_of_module', 'DataTable', 'read_txt',
]
