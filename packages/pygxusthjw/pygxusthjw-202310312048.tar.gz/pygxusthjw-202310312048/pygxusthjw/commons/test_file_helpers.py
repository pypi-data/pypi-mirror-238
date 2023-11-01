#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_file_helpers.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试file_helpers.py。
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
import os
import unittest

from . import array_utils
from . import gxusthjw_base
from .file_helpers import (FileInfo, get_file_encoding_chardet,
                           file_info, get_file_info,
                           get_file_info_of_module)


# ==================================================================
# noinspection DuplicatedCode
class TestFileHelpers(unittest.TestCase):
    """
    测试paths.py。
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

    def test_get_file_encoding_chardet(self):
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)

        test_data_folder = "test_data/file_helpers"
        test_data_path = os.path.join(this_file_path, test_data_folder)

        gkb_file = os.path.join(test_data_path, "gkb_file.txt")
        gkb_file_encoding = get_file_encoding_chardet(gkb_file)
        print("gkb_file_encoding(type({})):{}".format(type(gkb_file_encoding),
                                                      gkb_file_encoding))
        self.assertEquals(gkb_file_encoding, "GB2312")

        utf8_file = os.path.join(test_data_path, "utf8_file.txt")
        utf8_file_encoding = get_file_encoding_chardet(utf8_file)
        print("utf8_file_encoding(type({})):{}".format(type(utf8_file_encoding),
                                                       utf8_file_encoding))
        self.assertEquals(utf8_file_encoding, "utf-8")

        utf16_file = os.path.join(test_data_path, "utf16_file.txt")
        utf16_file_encoding = get_file_encoding_chardet(utf16_file)
        print("utf16_file_encoding(type({})):{}".format(type(utf16_file_encoding),
                                                        utf16_file_encoding))
        self.assertEquals(utf16_file_encoding, "UTF-16BE")

        utf16be_file = os.path.join(test_data_path, "utf16be_file.txt")
        utf16be_file_encoding = get_file_encoding_chardet(utf16be_file)
        print("utf16be_file_encoding(type({})):{}".format(type(utf16be_file_encoding),
                                                          utf16be_file_encoding))
        self.assertEquals(utf16be_file_encoding, "UTF-16BE")

        utf16le_file = os.path.join(test_data_path, "utf16le_file.txt")
        utf16le_file_encoding = get_file_encoding_chardet(utf16le_file)
        print("utf16le_file_encoding(type({})):{}".format(type(utf16le_file_encoding),
                                                          utf16le_file_encoding))
        self.assertEquals(utf16le_file_encoding, "UTF-16LE")

    def test_file_info(self):
        file = file_info("c:/", "a",
                         "txt", encoding="GBT", C="C",
                         O=20.2, E=True)
        print(file)
        self.assertEquals(str(file), "c:/a.txt")
        print(str(file))
        self.assertEquals(repr(file),
                          "FileInfo{'directory_path': 'c:/', "
                          "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                          "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                          "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEquals(file.C, "C")
        print(file.E)
        self.assertEquals(file.E, True)
        print(file.O)
        self.assertEquals(file.O, 20.2)

    def test_get_file_info(self):
        file = get_file_info('c:/a.txt', encoding="GBT", C="C",
                             O=20.2, E=True)
        print(file)
        self.assertEquals(str(file), "c:/a.txt")
        print(str(file))
        self.assertEquals(repr(file),
                          "FileInfo{'directory_path': 'c:/', "
                          "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                          "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                          "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEquals(file.C, "C")
        print(file.E)
        self.assertEquals(file.E, True)
        print(file.O)
        self.assertEquals(file.O, 20.2)

    def test_get_file_info_of_module(self):
        file = get_file_info_of_module(__name__)
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module(array_utils.__name__)
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module(gxusthjw_base.__name__)
        print(file)
        print(str(file))
        print(repr(file))

    # noinspection PyUnresolvedReferences
    def test_file_object_repr(self):
        file = FileInfo("c:/", "a",
                        "txt", encoding="GBT", C="C",
                        O=20.2, E=True)
        print(file)
        self.assertEquals(str(file), "c:/a.txt")
        print(str(file))
        self.assertEquals(repr(file),
                          "FileInfo{'directory_path': 'c:/', "
                          "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                          "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                          "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEquals(file.C, "C")
        print(file.E)
        self.assertEquals(file.E, True)
        print(file.O)
        self.assertEquals(file.O, 20.2)

    def test_make_file(self):
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)

        test_out = "test_out/file_helpers"

        dictionary_path = os.path.join(this_file_path, test_out)

        file = FileInfo(dictionary_path, "make_a_file1",
                        "txt", encoding="GBK", C="C",
                        O=20.2, E=True)

        # file.make_directory()
        file.make_file()


if __name__ == '__main__':
    unittest.main()
