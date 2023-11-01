#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_object_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试object_utils.py。
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
import unittest
from .object_utils import gen_hash, safe_repr
from .gxusthjw_base import Author, Version, Copyright


# ==================================================================


class TestObjectUtils(unittest.TestCase):
    """
    测试object_utils.py。
    """

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        print("\n\n-----------------------------------------------------")

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        print("-----------------------------------------------------")

    @classmethod
    def setUpClass(cls):
        """
        Hook method for setting up class fixture before running tests in the class.
        """
        print("\n\n=======================================================")

    @classmethod
    def tearDownClass(cls):
        """
        Hook method for deconstructing the class fixture after running all tests in the class.
        """
        print("=======================================================")

    def test_gen_hash(self):
        """
        测试arrays.hash_code方法。

        :return: None
        """
        print(gen_hash(0))
        print(gen_hash(0, 1))
        print(gen_hash(0, 1, 1.0, 2.0))
        print(gen_hash(0, object, "d"))
        print(gen_hash(0, 1, 1.0, 2.0, "dd"))
        print(gen_hash(0, 1, 1.0, 2.0, (1, 2, 3, 4)))

    def test_safe_repr(self):
        """
        测试safe_repr函数。
        """
        author = Author()
        version = Version()
        copyright1 = Copyright()
        print(safe_repr(author))
        print(safe_repr(version))
        print(safe_repr(copyright1))


if __name__ == '__main__':
    unittest.main()
