#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: pygxusthjw.commons包的__init__.py。
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
from .gxusthjw_base import (Base, Author, Version, Copyright)
from .array_utils import (hash_code, is_sorted,
                          is_sorted_ascending, is_sorted_descending,
                          reverse, Ordering, is_equals_of)
from .object_utils import (gen_hash, safe_repr)
from .path_utils import (join_file_path, sep_file_path)
from .math_plus import math_round
from .numpy_plus import (numpy_round, numpy_sech, numpy_cech,
                         numpy_coth, sech, cech, coth)
from .numerical_constant import (NUMERICAL_PRECISION, float_epsilon,
                                 ARITHMETIC_PRECISION, TINY_FLOAT,
                                 FLOAT_EPSILON, BOLTZMANN_CONSTANT,
                                 GAS_CONSTANT, AVOGADRO_CONSTANT)
from .statistical_interval import (IntervalRule, Interval,
                                   StatisticalInterval,
                                   IntervalGroup)
from .file_helpers import (FileInfo, get_file_encoding_chardet,
                           file_info, get_file_info,
                           get_file_info_of_module)
from .data_table import DataTable
from .file_reader import read_txt

# 定义 ============================================================
__version__ = "0.0.1"

__doc__ = """
The common functions and classes for pygxusthjw projects.
"""

__all__ = [
    'Base', 'Author', 'Version', 'Copyright',
    'hash_code', 'is_sorted',
    'is_sorted_ascending', 'is_sorted_descending', 'reverse',
    'Ordering', 'is_equals_of', 'gen_hash', 'safe_repr',
    'join_file_path', 'sep_file_path', 'math_round', 'numpy_round',
    'numpy_sech', 'numpy_cech', 'numpy_coth', 'sech', 'cech', 'coth',
    'NUMERICAL_PRECISION', 'ARITHMETIC_PRECISION', 'TINY_FLOAT',
    'FLOAT_EPSILON', 'float_epsilon', 'BOLTZMANN_CONSTANT',
    'GAS_CONSTANT', 'AVOGADRO_CONSTANT', 'IntervalRule', 'Interval',
    'StatisticalInterval', 'IntervalGroup', 'FileInfo',
    'get_file_encoding_chardet', 'file_info', 'get_file_info',
    'get_file_info_of_module', 'DataTable', 'read_txt',
]
