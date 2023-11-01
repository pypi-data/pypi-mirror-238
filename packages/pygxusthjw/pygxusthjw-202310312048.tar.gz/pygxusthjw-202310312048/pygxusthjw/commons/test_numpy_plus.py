#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_numpy_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试numpy_plus.py。
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

import numpy as np
from .numpy_plus import (numpy_round, numpy_sech, sech,
                         numpy_coth, coth, numpy_cech, cech)


# ==================================================================
class TestNumpyPlus(unittest.TestCase):
    """
    测试numpy_plus.py。
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

    def test_numpy_round(self):
        x = np.arange(1, 100)
        print(numpy_round(x))

    def test_hyperbolic(self):
        x = np.arange(1, 100)
        self.assertTrue(np.allclose(numpy_sech(x), sech(x)))

        print(numpy_cech(x))
        print(cech(x))
        print(numpy_coth(x))
        print(coth(x))

        self.assertTrue(np.allclose(numpy_cech(x), cech(x)))
        self.assertTrue(np.allclose(numpy_coth(x), coth(x)))


if __name__ == '__main__':
    unittest.main()
