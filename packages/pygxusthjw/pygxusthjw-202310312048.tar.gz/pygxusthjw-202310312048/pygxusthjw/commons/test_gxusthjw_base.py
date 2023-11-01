#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_gxusthjw_base.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试gxusthjw_base.py。
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

from .gxusthjw_base import Base, Author, Version, Copyright


# ==================================================================

class TestBase(unittest.TestCase):
    """
    测试`Base`类。
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

    def test_constructor(self):
        base = Base()
        print()
        print(base)
        print(base.author)
        print(base.version)
        print(base.copyright)

        author = Author("Jiwei Huang",
                        ("jiweihuang@vip.163.com",
                         "jiweihuang@yeah.net",
                         "huangjiwei@gxust.edu.cn"),
                        ("Guangxi University of Science and Technology",)
                        )
        version = Version(1, 0, 0, 0)

        self.assertEqual(base.author, author)
        self.assertEqual(base.version, version)
        self.assertEqual(base.copyright, Copyright())

        base2 = Base(author, version, Copyright())
        self.assertEqual(base, base2)


class TestAuthor(unittest.TestCase):
    """
    测试`Author`类。
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

    def test_name(self):
        author = Author("Jiwei Huang", ("jiweihuang@vip.163.com",
                                        "jiweihuang@yeah.net"),
                        ("Guangxi University of Science and Technology",))
        print()
        print(author.name)
        self.assertEqual("Jiwei Huang", author.name)
        print(author)
        print(author.__repr__())

    def test_email(self):
        print()
        author = Author("Jiwei Huang", ("jiweihuang@vip.163.com",
                                        "jiweihuang@yeah.net"),
                        ("Guangxi University of Science and Technology",))
        print(author.emails)
        self.assertTupleEqual(("jiweihuang@vip.163.com",
                               "jiweihuang@yeah.net"), author.emails)
        print(author)
        print(author.__repr__())

    def test_organization(self):
        print()
        author = Author("Jiwei Huang", ("jiweihuang@vip.163.com",
                                        "jiweihuang@yeah.net"),
                        ("Guangxi University of Science and Technology",))
        print(author.organizations)
        self.assertTupleEqual(("Guangxi University of Science and Technology",),
                              author.organizations)
        print(author)
        print(author.__repr__())


class TestVersion(unittest.TestCase):
    """
    测试`Version`类。
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

    def test_constructor(self):
        self.assertRaises(ValueError, Version.__init__, self, -1, 2, 3, 4)
        self.assertRaises(ValueError, Version.__init__, self, 1, -2, 3, 4)
        self.assertRaises(ValueError, Version.__init__, self, 1, 2, -3, 4)
        self.assertRaises(ValueError, Version.__init__, self, 1, 2, 3, -4)

    def test_major(self):
        version = Version(1, 2, 3, 5)
        print()
        print(version)
        print(version.__repr__())
        self.assertEqual(1, version.major)

    def test_minor(self):
        version = Version(1, 2, 3, 5)
        print()
        print(version)
        print(version.__repr__())
        self.assertEqual(2, version.minor)

    def test_build(self):
        version = Version(1, 2, 3, 5)
        print()
        print(version)
        print(version.__repr__())
        self.assertEqual(3, version.build)

    def test_revision(self):
        version = Version(1, 2, 3, 5)
        print()
        print(version)
        print(version.__repr__())
        self.assertEqual(5, version.revision)


class TestCopyright(unittest.TestCase):
    """
    测试`Copyright`类。
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

    def test_constructor(self):
        """
        测试Copyright的初始化方法。
        """
        copy = Copyright()
        print()
        print(copy)
        self.assertEqual(
            "Copyright{statement=Copyright (c) 2016-2023, Jiwei Huang. All Rights Reserved.,agreements=()}",
            copy.__str__())
        print(copy.statement)
        self.assertEqual("Copyright (c) 2016-2023, Jiwei Huang. All Rights Reserved.", copy.statement)
        print(copy.agreements)
        print(copy.__repr__())
        print(hash(copy))


if __name__ == '__main__':
    unittest.main()
