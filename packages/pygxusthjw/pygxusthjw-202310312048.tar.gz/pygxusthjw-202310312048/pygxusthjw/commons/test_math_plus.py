#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_math_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试math_plus.py。
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
from .math_plus import math_round


# ==================================================================
class TestMathPlus(unittest.TestCase):
    """
    测试math_plus.py。
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

    def test_round(self):
        self.assertEqual(0, round(0.0))
        self.assertEqual(0, round(0.2))
        self.assertEqual(0, round(0.3))
        self.assertEqual(0, round(0.4))

        # 奇怪的结果如下：
        self.assertEqual(0, round(0.5))
        self.assertEqual(0, round(0.500000000000000001))
        self.assertEqual(1, round(0.5000000000000001))

        self.assertEqual(1, round(0.6))
        self.assertEqual(1, round(0.7))
        self.assertEqual(1, round(0.8))
        self.assertEqual(1, round(0.9))
        self.assertEqual(1, round(1.0))

        self.assertEqual(2, round(1.5))

        self.assertEqual(2, round(1.6))
        self.assertEqual(2, round(1.7))
        self.assertEqual(2, round(1.8))
        self.assertEqual(2, round(1.9))

    def test_math_round(self):
        self.assertEqual(1, math_round(0.5))

        self.assertEqual(1, math_round(0.500000000000000001))
        self.assertEqual(1, math_round(0.5000000000000001))

        self.assertEqual(1, math_round(0.500000000000000000000000000000000001))


if __name__ == '__main__':
    unittest.main()
