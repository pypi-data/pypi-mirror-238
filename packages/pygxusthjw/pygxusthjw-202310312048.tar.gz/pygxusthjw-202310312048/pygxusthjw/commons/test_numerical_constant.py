#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_numerical_constant.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试numerical_constant.py。
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

from .numerical_constant import (NUMERICAL_PRECISION,
                                 float_epsilon, ARITHMETIC_PRECISION,
                                 TINY_FLOAT, FLOAT_EPSILON,
                                 BOLTZMANN_CONSTANT, GAS_CONSTANT,
                                 AVOGADRO_CONSTANT)


# ==================================================================


class TestNumericalConstant(unittest.TestCase):
    """
    测试numerical_constant.py。
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

    def test_numerical_precision(self):
        print("\n")
        print("========================================\n")
        print("NUMERICAL_PRECISION=%g" % NUMERICAL_PRECISION)
        print("========================================\n")
        assert NUMERICAL_PRECISION == 1E-9

    def test_arithmetic_precision(self):
        print("\n")
        print("========================================\n")
        print("ARITHMETIC_PRECISION=%g" % ARITHMETIC_PRECISION)
        print("========================================\n")
        assert ARITHMETIC_PRECISION == 1E-6
        assert TINY_FLOAT == 1e-15

    def test_float_epsilon(self):
        print("\n")
        print("========================================\n")
        print("FLOAT_EPSILON=%g" % FLOAT_EPSILON)
        print("float_epsilon()=%g" % float_epsilon())
        print("========================================\n")
        assert FLOAT_EPSILON == 2.220446049250313E-16
        assert float_epsilon() == 2.220446049250313E-16
        assert FLOAT_EPSILON == float_epsilon()

    def test_boltzmann_gas_avogadro_constant(self):
        """
        测试玻尔兹曼常数。
        玻尔兹曼常数的物理意义是：气体常数R是玻尔兹曼常量k乘上阿伏伽德罗常量N_A。
        即 R=k*N_A
        """
        gas_constant = BOLTZMANN_CONSTANT * AVOGADRO_CONSTANT
        print("\n")
        print("===========================================\n")
        print("GAS_CONSTANT=%g" % GAS_CONSTANT)
        print("BOLTZMANN_CONSTANT=%g" % BOLTZMANN_CONSTANT)
        print("AVOGADRO_CONSTANT=%g" % AVOGADRO_CONSTANT)
        print("gas_constant=%g" % gas_constant)
        print("===========================================\n")
        assert BOLTZMANN_CONSTANT == 1.380649E-23
        assert GAS_CONSTANT == 8.314
        assert AVOGADRO_CONSTANT == 6.02214076E23
        assert GAS_CONSTANT - gas_constant < 1E-6


if __name__ == '__main__':
    unittest.main()
