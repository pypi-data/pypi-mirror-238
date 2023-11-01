#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_array_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试array_utils.py。
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
from .array_utils import (hash_code, is_sorted,
                          is_sorted_ascending, is_sorted_descending,
                          reverse, Ordering, is_equals_of)


# ==================================================================

class TestArrayUtils(unittest.TestCase):
    """
    测试array_utils.py。
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

    def test_hash_code(self):
        """
        测试arrays.hash_code方法。

        :return: None
        """
        print(hash_code(0))
        print(hash_code(0, 1))
        print(hash_code(0, 1, 1.0, 2.0))
        print(hash_code(0, object, "d"))
        print(hash_code(0, 1, 1.0, 2.0, "dd"))
        print(hash_code(0, 1, 1.0, 2.0, (1, 2, 3, 4)))

    def test_is_sorted(self):
        x1 = [1, 2, 3, 4, 5, 6, 8, 10, 110]
        self.assertEqual(True, is_sorted(x1))
        self.assertEqual(True, is_sorted_ascending(x1))
        self.assertEqual(False, is_sorted_descending(x1))

        x1_r = reverse(x1)
        self.assertEqual(True, is_sorted(x1_r))
        self.assertEqual(False, is_sorted_ascending(x1_r))
        self.assertEqual(True, is_sorted_descending(x1_r))
        print()
        print(x1_r)

    def test_ordering(self):
        print(Ordering['unordered'])
        print(Ordering['unordered'].value)
        print(Ordering['ascending'].value)
        print(Ordering['ascending'])
        print(Ordering['descending'].value)
        print(Ordering['descending'])

    def test_is_equals_of(self):
        a = [1.0, 2.0, 3.0, 4.0]
        self.assertTrue(is_equals_of(a, a))


if __name__ == '__main__':
    unittest.main()
