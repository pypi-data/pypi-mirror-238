#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        statistical_interval.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义'数据区间'。
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
from enum import Enum
from typing import Union

import numpy as np

# ==================================================================
# 定义使用字符串获取IntervalRule枚举对象时，可解析的字符串。
recognizable_open_open_str = ["()", "open_open", "OPEN_OPEN",
                              "openOpen", "Openopen", "openopen",
                              "OpenOpen", "OPENOPEN"]
recognizable_open_close_str = ["(]", "open_close", "OPEN_CLOSE",
                               "openClose", "Openclose", "openclose",
                               "OpenClose", "OPENCLOSE"]
recognizable_close_open_str = ["[)", "close_open", "CLOSE_OPEN",
                               "closeOpen", "Closeopen", "closeopen",
                               "CloseOpen", "CLOSEOPEN"]
recognizable_close_close_str = ["[]", "close_close", "CLOSE_CLOSE",
                                "closeClose", "Closeclose", "closeclose",
                                "CloseClose", "CLOSECLOSE"]


class IntervalRule(Enum):
    """
    类`IntervalRule`表征区间规则。
    """

    # 前开后开
    OpenOpen = 0
    """
    前开后开
    """

    # 前开后闭
    OpenClose = 1
    """
    前开后闭
    """

    # 前闭后开
    CloseOpen = 2
    """
    前闭后开
    """

    # 前闭后闭
    CloseClose = 3
    """
    前闭后闭
    """

    # noinspection PyUnresolvedReferences
    @staticmethod
    def from_string(rule_str):
        """
        从字符串构建区间规则。

        :param rule_str: 区间规则字符串。
        :return: `IntervalRule`
        """
        if rule_str in recognizable_open_open_str:
            return IntervalRule.OpenOpen
        elif rule_str in recognizable_open_close_str:
            return IntervalRule.OpenClose
        elif rule_str in recognizable_close_open_str:
            return IntervalRule.CloseOpen
        elif rule_str in recognizable_close_close_str:
            return IntervalRule.CloseClose
        else:
            raise ValueError("Unrecognized parameter value for %s" % rule_str)

    @staticmethod
    def is_fore_open(interval_rule) -> bool:
        """
        判断指定的区间规则是否为前开区间。

        :param interval_rule: 区间规则。
        :type interval_rule: `IntervalRule`
        :return: 如果是前开区间返回True，否则返回False。
        """
        return interval_rule == IntervalRule.OpenOpen or \
            interval_rule == IntervalRule.OpenClose

    @staticmethod
    def is_fore_close(interval_rule) -> bool:
        """
        判断指定的区间规则是否为前闭区间。

        :param interval_rule: 区间规则。
        :type interval_rule: `IntervalRule`
        :return: 如果是前闭区间返回True，否则返回False。
        """
        return interval_rule == IntervalRule.CloseOpen or \
            interval_rule == IntervalRule.CloseClose

    @staticmethod
    def is_back_open(interval_rule) -> bool:
        """
        判断指定的区间规则是否为后开区间。

        :param interval_rule: 区间规则。
        :type interval_rule: `IntervalRule`
        :return: 如果是后开区间返回True，否则返回False。
        """
        return interval_rule == IntervalRule.OpenOpen or \
            interval_rule == IntervalRule.CloseOpen

    @staticmethod
    def is_back_close(interval_rule) -> bool:
        """
        判断指定的区间规则是否为后闭区间。

        :param interval_rule: 区间规则。
        :type interval_rule: `IntervalRule`
        :return: 如果是后闭区间返回True，否则返回False。
        """
        return interval_rule == IntervalRule.OpenClose or \
            interval_rule == IntervalRule.CloseClose


class Interval(object):
    """
    类`Interval`表征区间。
    """

    def __init__(self, lower_limit: Union[int, float],
                 upper_limit: Union[int, float],
                 rule: IntervalRule = IntervalRule.CloseClose,
                 index: int = 0):
        """
        类`Interval`的初始化方法。

        :param lower_limit: 区间下限。
        :param upper_limit: 区间上限。
        :param rule: 区间规则。
        :param index: 区间的index值（可选）。
        """
        if lower_limit >= upper_limit:
            raise ValueError("Expected lower_limit < upper_limit, "
                             "but got lower_limit=%d, upper_limit=%d" % lower_limit,
                             upper_limit)

        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit

        self.__rule = rule

        self.__index = index

    @property
    def lower_limit(self) -> Union[int, float]:
        """
        获取区间下限。

        :return: 区间下限。
        :rtype: Union[int, float]
        """
        return self.__lower_limit

    @property
    def upper_limit(self) -> Union[int, float]:
        """
        获取区间上限。

        :return: 区间上限。
        :rtype: Union[int, float]
        """
        return self.__upper_limit

    @property
    def rule(self) -> IntervalRule:
        """
        获取区间规则。

        :return: 区间规则。
        :rtype: IntervalRule
        """
        return self.__rule

    @property
    def index(self):
        """
        获取 区间的index值（可选）。

        :return:  区间的index值（可选）。
        :rtype: int
        """
        return self.__index

    def check(self, value) -> bool:
        """
        判断指定值是否在此区间。

        :param value: 要判断的直。
        :return: 如果指定值在此区间，返回True，否则返回False。
        """
        if self.rule == IntervalRule.OpenOpen:
            return self.lower_limit < value < self.upper_limit
        elif self.rule == IntervalRule.OpenClose:
            return self.lower_limit < value <= self.upper_limit
        elif self.rule == IntervalRule.CloseOpen:
            return self.lower_limit <= value < self.upper_limit
        elif self.rule == IntervalRule.CloseClose:
            return self.lower_limit <= value <= self.upper_limit
        else:
            raise ValueError("Unrecognized InternalRule for %s" % self.rule)

    def check2(self, value, atol=1e-9):
        """
        判断指定值是否在此区间。

        :param atol: 绝对误差。
        :param value: 要判断的直。
        :return: 如果指定值在此区间，返回True，否则返回False。
        """
        atol = abs(atol)
        if self.rule == IntervalRule.OpenOpen:
            return self.lower_limit - atol < value < self.upper_limit + atol
        elif self.rule == IntervalRule.OpenClose:
            return self.lower_limit - atol < value < self.upper_limit + atol
        elif self.rule == IntervalRule.CloseOpen:
            return self.lower_limit - atol < value < self.upper_limit + atol
        elif self.rule == IntervalRule.CloseClose:
            return self.lower_limit - atol < value < self.upper_limit + atol
        else:
            raise ValueError("Unrecognized InternalRule for %s" % self.rule)

    def __str__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        if self.rule == IntervalRule.OpenOpen:
            return "(%d,%d)" % (self.lower_limit, self.upper_limit)
        elif self.rule == IntervalRule.OpenClose:
            return "(%d,%d]" % (self.lower_limit, self.upper_limit)
        elif self.rule == IntervalRule.CloseOpen:
            return "[%d,%d)" % (self.lower_limit, self.upper_limit)
        elif self.rule == IntervalRule.CloseClose:
            return "[%d,%d]" % (self.lower_limit, self.upper_limit)
        else:
            raise ValueError("Unrecognized InternalRule for %s" % self.rule)

    def __repr__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return self.__str__()


class StatisticalInterval(Interval):
    """
    类`StatisticalInterval`表征"统计区间"。
    """

    def __init__(self, lower_limit: Union[int, float],
                 upper_limit: Union[int, float],
                 rule: IntervalRule = IntervalRule.CloseClose,
                 index: int = 0):
        """
        类`StatisticalInterval`初始化方法。

        :param lower_limit: 区间下限。
        :param upper_limit: 区间上限。
        :param rule: 区间规则。
        """
        super(StatisticalInterval, self).__init__(lower_limit,
                                                  upper_limit,
                                                  rule,
                                                  index)
        self.__values = []

    @property
    def frequency_num(self):
        """
        获取此区间中值的频数。

        :return: 此区间中值的频数。
        """
        return self.__len__()

    def update(self, value, atol=None) -> bool:
        """
        将指定值添加至此区间中。

        :param atol: 绝对误差。
        :param value: 要添加的值。
        :return: 如果添加成功返回True，否则返回False。
        """
        if atol is None:
            if self.check(value):
                self.__values.append(value)
                return True
            else:
                return False
        else:
            if self.check2(value, atol):
                self.__values.append(value)
                return True
            else:
                return False

    def __len__(self):
        """
        计算添加到此区间的值的数量。

        :return: 此区间的值的数量。
        """
        return self.__values.__len__()

    def __iter__(self):
        """
        获取统计区间中数据的迭代对象。

        :return:  迭代器。
        """
        return self.__values.__iter__()

    def __str__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        if self.rule == IntervalRule.OpenOpen:
            return "{{({},{}):{}}}".format(self.lower_limit, self.upper_limit, self.frequency_num)
        elif self.rule == IntervalRule.OpenClose:
            return "{{({},{}]:{}}}".format(self.lower_limit, self.upper_limit, self.frequency_num)
        elif self.rule == IntervalRule.CloseOpen:
            return "{{[{},{}):{}}}".format(self.lower_limit, self.upper_limit, self.frequency_num)
        elif self.rule == IntervalRule.CloseClose:
            return "{{[{},{}]:{}}}".format(self.lower_limit, self.upper_limit, self.frequency_num)
        else:
            raise ValueError("Unrecognized InternalRule for %s" % self.rule)

    def __repr__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return self.__str__()


# noinspection PyTypeChecker
class IntervalGroup(object):
    """
    类`IntervalGroup`表征“区间分组”。
    """

    def __init__(self, start: float, end: float, num: int,
                 interval_rule: IntervalRule = IntervalRule.CloseClose,
                 mid_interval_rule: IntervalRule = IntervalRule.OpenClose):
        """
        类`IntervalGroup`的初始化方法。

        :param start: 区间分组的起点。
        :param end: 区间分组的终点。
        :param num: 区间分组的组数。
        :param interval_rule:区间分组的规则。
        :param mid_interval_rule: 中间区间的规则。
        """
        # 要求区间分组的两端点不相等。
        if start == end:
            raise ValueError(
                "Expected start is not equal to end,"
                "but got start={},end={}.".format(
                    start, end))
        self.__start = start
        self.__end = end

        # 要求num>=0
        if num < 1:
            raise ValueError("Expected num >= 1,"
                             "but got num = {}.".format(num))
        self.__num = num

        self.__interval_rule = interval_rule

        # 要求中间规则只能是前开后闭或前闭后开。
        if not (mid_interval_rule == IntervalRule.OpenClose or
                mid_interval_rule == IntervalRule.CloseOpen):
            raise ValueError("Expected mid_interval_rule must be one of {{OpenClose,CloseOpen}},"
                             "but got mid_interval_rule={}.".format(mid_interval_rule))
        self.__mid_interval_rule = mid_interval_rule

        steps = np.linspace(start, end, num + 1, endpoint=True)
        print(steps)
        intervals = dict()
        for i in range(1, len(steps)):
            lower = steps[i - 1]
            # print(lower)
            upper = steps[i]
            # print(upper)
            rule = self.__mid_interval_rule
            if i == 1:
                if IntervalRule.is_fore_open(interval_rule):
                    if self.__mid_interval_rule == IntervalRule.OpenClose:
                        rule = IntervalRule.OpenClose
                    else:
                        rule = IntervalRule.OpenOpen
                else:
                    if self.__mid_interval_rule == IntervalRule.OpenClose:
                        rule = IntervalRule.CloseClose
                    else:
                        rule = IntervalRule.CloseOpen
            elif i == (len(steps) - 1):
                if IntervalRule.is_back_open(interval_rule):
                    if self.__mid_interval_rule == IntervalRule.OpenClose:
                        rule = IntervalRule.OpenOpen
                    else:
                        rule = IntervalRule.CloseOpen
                else:
                    if self.__mid_interval_rule == IntervalRule.OpenClose:
                        rule = IntervalRule.OpenClose
                    else:
                        rule = IntervalRule.CloseClose
            else:
                pass

            intervals[i - 1] = StatisticalInterval(lower, upper, rule, i - 1)

        self.__intervals = intervals
        self.__values = list()

    @property
    def start(self):
        """
        获取区间分组的起点。

        :return: 区间分组的起点。
        """
        return self.__start

    @property
    def end(self):
        """
        获取区间分组的终点。

        :return: 区间分组的终点。
        """
        return self.__end

    @property
    def num(self):
        """
        获取区间分组的组数。

        :return: 区间分组的组数。
        """
        return self.__num

    @property
    def interval_rule(self):
        """
        获取区间分组的规则。

        :return: 区间分组的规则。
        """
        return self.__interval_rule

    @property
    def mid_interval_rule(self):
        """
        获取中间区间的规则。

        :return: 中间区间的规则。
        """
        return self.__mid_interval_rule

    def update(self, value, atol=None):
        """
        将指定值添加至分组区间。

        :param value: 指定的值。
        :param atol: 绝对误差。
        :return: 添加成功则返回True，否则返回False。
        """
        flag = False
        for i in range(self.num):
            if i == 0 or i == self.num - 1:
                if self.__intervals[i].update(value, atol=atol):
                    flag = True
                    break
            else:
                if self.__intervals[i].update(value):
                    flag = True
                    break
        if flag:
            self.__values.append(value)
            return True
        else:
            return False

    @property
    def values_num(self):
        """
        获取添加值的总个数。

        :return: 添加值的总个数。
        """
        return len(self.__values)

    @property
    def frequency_num(self):
        """
        获取各分组的频数。

        :return: 各分组的频数。
        """
        fn = dict()
        for key, interval in self.__intervals.items():
            fn[key] = interval.frequency_num
        return fn

    @property
    def frequency_rate(self):
        """
        获取各分组的频率。

        :return: 各分组的频率。
        """
        fr = dict()
        for key, fn in self.frequency_num.items():
            fr[key] = fn / self.values_num
        return fr

    def get_interval(self, index: int):
        """
        获取指定index的统计区间。

        :param index: 指定的索引值。
        :return: 统计区间对象。
        """
        return self.__intervals[index]

    def get_frequency_rate(self, index: int):
        """
        获取指定index的统计区间的频率。

        :param index: 指定的索引值。
        :return: 频率。
        """
        return self.get_interval(index) / self.values_num

    def get_frequency_num(self, index: int):
        """
        获取指定index的统计区间的频数。

        :param index: 指定的索引值。
        :return: 频数。
        """
        return self.get_interval(index).frequency_num

    def __str__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return "{}".format(self.__intervals)

    def __repr__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return self.__str__()
