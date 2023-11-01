#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_statistical_interval.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试statistical_interval.py。
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
from unittest import TestCase
from .statistical_interval import (IntervalRule, Interval,
                                   StatisticalInterval, IntervalGroup)


# ==================================================================
class TestIntervalRule(TestCase):
    """
    测试IntervalRule。
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

    def test_from_string(self):
        print(IntervalRule.from_string("()"))
        print(IntervalRule.from_string("(]"))
        print(IntervalRule.from_string("[)"))
        print(IntervalRule.from_string("[]"))

        print(IntervalRule.from_string("open_open"))
        print(IntervalRule.from_string("open_close"))
        print(IntervalRule.from_string("close_open"))
        print(IntervalRule.from_string("close_close"))
        print(IntervalRule.from_string("openopen"))
        print(IntervalRule.from_string("openclose"))
        print(IntervalRule.from_string("closeopen"))
        print(IntervalRule.from_string("closeclose"))

    def test_is(self):
        self.assertFalse(IntervalRule.is_back_close(IntervalRule.from_string("()")))
        self.assertTrue(IntervalRule.is_back_close(IntervalRule.from_string("(]")))
        self.assertFalse(IntervalRule.is_back_close(IntervalRule.from_string("[)")))
        self.assertTrue(IntervalRule.is_back_close(IntervalRule.from_string("[]")))

        self.assertTrue(IntervalRule.is_back_open(IntervalRule.from_string("()")))
        self.assertFalse(IntervalRule.is_back_open(IntervalRule.from_string("(]")))
        self.assertTrue(IntervalRule.is_back_open(IntervalRule.from_string("[)")))
        self.assertFalse(IntervalRule.is_back_open(IntervalRule.from_string("[]")))

        self.assertFalse(IntervalRule.is_fore_close(IntervalRule.from_string("()")))
        self.assertFalse(IntervalRule.is_fore_close(IntervalRule.from_string("(]")))
        self.assertTrue(IntervalRule.is_fore_close(IntervalRule.from_string("[)")))
        self.assertTrue(IntervalRule.is_fore_close(IntervalRule.from_string("[]")))

        self.assertTrue(IntervalRule.is_fore_open(IntervalRule.from_string("()")))
        self.assertTrue(IntervalRule.is_fore_open(IntervalRule.from_string("(]")))
        self.assertFalse(IntervalRule.is_fore_open(IntervalRule.from_string("[)")))
        self.assertFalse(IntervalRule.is_fore_open(IntervalRule.from_string("[]")))


class TestInterval(TestCase):
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
        interval1 = Interval(0, 1, IntervalRule.OpenClose)
        print(interval1)

        interval2 = Interval(0, 1, IntervalRule.OpenOpen)
        print(interval2)

        interval3 = Interval(0, 1, IntervalRule.CloseOpen)
        print(interval3)

        interval4 = Interval(0, 1, IntervalRule.CloseClose)
        print(interval4)

    # noinspection DuplicatedCode
    def test_is_check(self):
        interval1 = Interval(0, 1, IntervalRule.OpenClose)
        print(interval1.check(0))
        print(interval1.check(1))

        interval2 = Interval(0, 1, IntervalRule.OpenOpen)
        print(interval2.check(0))
        print(interval2.check(1))

        interval3 = Interval(0, 1, IntervalRule.CloseOpen)
        print(interval3.check(0))
        print(interval3.check(1))

        interval4 = Interval(0, 1, IntervalRule.CloseClose)
        print(interval4.check(0))
        print(interval4.check(1))


class TestIntervalGroup(TestCase):
    """
    测试IntervalGroup。
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
        ig = IntervalGroup(0, 10, 9,
                           interval_rule=IntervalRule.CloseClose)
        print(ig)

        ig = IntervalGroup(0, 10, 10,
                           interval_rule=IntervalRule.CloseClose)
        print(ig)

        ig = IntervalGroup(0, 10, 11,
                           interval_rule=IntervalRule.CloseClose)
        print(ig)

        ig = IntervalGroup(0, 10, 11,
                           interval_rule=IntervalRule.CloseClose,
                           mid_interval_rule=IntervalRule.CloseOpen)
        print(ig)

        ig = IntervalGroup(0, 10, 11,
                           interval_rule=IntervalRule.CloseOpen,
                           mid_interval_rule=IntervalRule.CloseOpen)
        print(ig)

    def test_update(self):
        ig = IntervalGroup(0, 10, 11,
                           interval_rule=IntervalRule.CloseClose,
                           mid_interval_rule=IntervalRule.CloseOpen)
        import random
        for i in range(1000):
            value = random.randint(0, 10)
            ig.update(value)

        print(ig.frequency_rate)

        ig = IntervalGroup(0, 100, 21,
                           interval_rule=IntervalRule.CloseClose,
                           mid_interval_rule=IntervalRule.CloseOpen)
        import random
        for i in range(1000):
            value = random.uniform(0, 100)
            ig.update(value)

        print(ig.frequency_rate)


if __name__ == '__main__':
    unittest.main()
