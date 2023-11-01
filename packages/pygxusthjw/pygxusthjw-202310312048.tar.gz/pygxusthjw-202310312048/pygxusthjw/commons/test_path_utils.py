#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_path_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试path_utils.py。
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
import os.path
import unittest
from .path_utils import join_file_path, sep_file_path


# ==================================================================
class TestPathUtils(unittest.TestCase):
    """
    测试path_utils.py。
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

    def test_join_file_path(self):
        path = "c:/a"
        file_name = "b"
        file_type = ".pdf"
        print(join_file_path(path, file_name, file_type))
        file_type = "pdf"
        print(join_file_path(path, file_name, file_type))

    def test_sep_file_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test_folder = "test_data"
        path = os.path.join(path, test_folder)
        file_name = "b"
        file_type = ".pdf"
        print(join_file_path(path, file_name, file_type))
        print(sep_file_path(join_file_path(path, file_name, file_type),
                            with_dot_in_ext=False))


if __name__ == '__main__':
    unittest.main()
