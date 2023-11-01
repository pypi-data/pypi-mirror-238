#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        numerical_constant.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 承载一些数值常量。
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
# 导包 ==============================================================

# 定义 ==============================================================
# 数值精度（numerical precision）：1e-9。
NUMERICAL_PRECISION = 1E-9

# 算术精度（Arithmetic Precision）：1e-6
ARITHMETIC_PRECISION = 1E-6

# 依据IEEE-754 标准，float型数值的机器精度。
# 此数值的计算方法见float_epsilon()。
# Python中只有一种浮点数，即float。
FLOAT_EPSILON = 2.220446049250313E-16

# 一个极小的数。
TINY_FLOAT = 1.e-15

# 玻尔兹曼常数（Boltzmann constant），记为“k”或“kB”，是关于温度及能量的一个物理常数。
# 数值为：k=1.380649 × 10^-23，单位：J/K
# 玻尔兹曼常数的物理意义是：气体常数R 是玻尔兹曼常量k乘上阿伏伽德罗常量N_A。
# Reference：https://baike.baidu.com/item/%E7%8E%BB%E5%B0%94%E5%85%B9%E6%9B%BC%E5%B8%B8%E6%95%B0?sefr=enterbtn
BOLTZMANN_CONSTANT = 1.380649E-23

# 理想气体常数（Gas constant），又名“通用气体常数”，记为“R”，是一个在物态方程中联系各个热力学函数的物理常数。
# 在法定计量单位中，R=8.314，单位：J·mol^-1·K^-1
# Reference：https://baike.baidu.com/item/%E7%90%86%E6%83%B3%E6%B0%94%E4%BD%93%E5%B8%B8%E6%95%B0
GAS_CONSTANT = 8.314

# 阿伏伽德罗常量（Avogadro constant），又名“阿伏伽德罗常数”，为热学常量，符号为N_A。
# 它的精确数值为：6.02214076×10^23，一般计算时取：6.02×10^23或6.022×10^23，单位：mol^-1
# Reference：https://baike.baidu.com/item/%E9%98%BF%E4%BC%8F%E4%BC%BD%E5%BE%B7%E7%BD%97%E5%B8%B8%E9%87%8F/1941738?fromtitle=%E9%98%BF%E4%BC%8F%E4%BC%BD%E5%BE%B7%E7%BD%97%E5%B8%B8%E6%95%B0&fromid=5058420
AVOGADRO_CONSTANT = 6.02214076E23


def float_epsilon():
    """
    计算float型数值的机器精度。

    :return: float型数值的机器精度。
    """
    value: float = 1.0
    while 1.0 < (1.0 + value):
        value = value / 2.0
    return 2.0 * value
