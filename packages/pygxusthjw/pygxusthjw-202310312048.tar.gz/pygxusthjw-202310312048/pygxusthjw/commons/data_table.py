#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        data_table.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义表征“数据表”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/18     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Optional, Union

import numpy as np
import pandas as pd

# 定义 ==============================================================

# 缺省的列名前缀。
DEFAULT_COL_NAME_PREFIX = "col_"


class DataTable(object):
    """
    类`DataTable`表征“数据表”。
    """

    def __init__(self, *args, **kwargs):
        """
        类`DataTable`的初始化方法。


            1. 对于可变参数args，其作用是初始化数据项，args中的每个元素为1个数据项。

                args中每个元素的允许值包括：

                （1）标量值，类型必须为int,float,bool,str或object等。

                （2）类数组值： 类型必须为list，tuple，numpy.ndarray等。

            2. 对于可变关键字参数kwargs，为指定的初始化数据项指定名称：

                （1）通过 col_names关键字参数，如果其为字典，则键对应数据项的序号，而值对应数据项名。

                （2）通过 col_names关键字参数，如果其为列表或元组，则序号对应数据项的序号，而值对应数据项名。

                （3）如果没有指定col_names关键字参数或者col_names不符合（1）和（2）的规则，则采用缺省的列名。

            3. 任何数据项名的遗漏，都会以col_i的形式代替。

        :param args: 可选的数据列元组。
        :param kwargs: 可选的关键字参数。
        """
        # 数据表对象中的数据，被保存为pandas.DataFrame格式。
        # 私有实例变量`__data`用于保存数据表对象中的数据。
        self.__data = pd.DataFrame()

        # 初始化数据表的列数。
        col_count = len(args)
        col_names = {}
        if "col_names" in kwargs and kwargs["col_names"] is not None:
            kwargs_col_names = kwargs["col_names"]

            # 如果指定列名时，使用的是字典。
            if isinstance(kwargs_col_names, dict):
                for key in kwargs_col_names.keys():
                    # 字典的键必须是整数，这个整数代表数据项的序号。
                    if not isinstance(key, int):
                        raise ValueError("the key of col_names must be a int value,"
                                         "but got {}".format(key))
                    # 如果键值超过了初始数据项的数量，则跳过。
                    if key >= col_count:
                        continue
                    key_col_name = kwargs_col_names[key]
                    # 如果字典值类型不是None，则设置为数据项名。
                    if key_col_name is not None:
                        if isinstance(key_col_name, str):
                            col_names[key] = key_col_name
                        else:
                            col_names[key] = str(key_col_name)
                    else:
                        col_names[key] = "{}{}".format(DEFAULT_COL_NAME_PREFIX, key)
            elif isinstance(kwargs_col_names, (list, tuple)):
                for col_index in range(len(kwargs_col_names)):
                    if col_index >= col_count:
                        break
                    col_name = kwargs_col_names[col_index]
                    if col_name is not None:
                        if isinstance(col_name, str):
                            col_names[col_index] = col_name
                        else:
                            col_names[col_index] = str(col_name)
                    else:
                        col_names[col_index] = "{}{}".format(DEFAULT_COL_NAME_PREFIX, col_index)
            else:
                raise ValueError("The type of col_names must be one of {{dict,list,tuple}}")
        else:
            for col_index in range(col_count):
                col_names[col_index] = "{}{}".format(DEFAULT_COL_NAME_PREFIX, col_index)

        # 补充遗漏
        for col_index in range(col_count):
            if col_index in col_names.keys():
                continue
            else:
                col_names[col_index] = "{}{}".format(DEFAULT_COL_NAME_PREFIX, col_index)

        if len(col_names) != 0:
            make_list = list()
            for col_index in range(col_count):
                col_value = args[col_index]
                # 检查args[i]是否为标量，如果是，在构造DataFrame时，必须给index
                if np.isscalar(col_value):
                    make_list.append(pd.DataFrame({col_names[col_index]: col_value}, index=[0]))
                elif isinstance(col_value, (list, tuple, pd.Series, np.ndarray)):
                    make_list.append(pd.DataFrame({col_names[col_index]: np.array(col_value, copy=True)}))
                else:
                    make_list.append(pd.DataFrame({col_names[col_index]: [col_value, ]}, index=[0]))
            self.__data = pd.concat(make_list, axis=1)

        for key in kwargs.keys():
            if hasattr(self, key):
                continue
            else:
                setattr(self, key, kwargs[key])

    @property
    def data(self):
        """
        获取数据表中的数据。

        :return: pandas.DataFrame
        """
        return self.__data

    def get_col(self, col_index: Union[str, int]):
        """
        获取指定列索引的列。

        :param col_index: 索引。
        :return: 列对象。
        """
        if isinstance(col_index, int):
            return self.__data.iloc[:, col_index].dropna()
        else:
            return self.__data[col_index].dropna()

    def add_col(self, col_value, col_name=None):
        """
        添加列。

        :param col_name: 列名。
        :param col_value: 列对象。
        :return:
        """
        if col_name is None:
            num_col = self.shape[1]
            col_name = "{}{}".format(DEFAULT_COL_NAME_PREFIX, num_col)

        if not isinstance(col_name, str):
            raise ValueError("the type of col_name must be a str,"
                             "but got {}.".format(col_name))

        if np.isscalar(col_value):
            new_frame = pd.DataFrame({col_name: col_value}, index=[0])
        elif isinstance(col_value, (list, tuple, pd.Series, np.ndarray)):
            new_frame = pd.DataFrame({col_name: np.array(col_value, copy=True)})
        else:
            new_frame = pd.DataFrame({col_name: [col_value, ]}, index=[0])

        # 判断self.__data是否为空。
        if len(self.__data.index) == 0:
            self.__data = new_frame
        else:
            self.__data = pd.concat([self.__data, new_frame], axis=1)

    @property
    def shape(self):
        """
        获取数据表的形状。

        :return: 元组（行数，列数）
        """
        return self.__data.shape

    def print_data(self, options: Optional[dict]):
        """
        print数据。

        :param options: 用于设置set_option的键和值。
        :return: None
        """
        if options:
            for key in options.keys():
                pd.set_option(key, options[key])

        print(self.__data)

    def to_csv(self, **kwargs):
        """
        数据输出至csv格式文件。

        :param kwargs: pandas.to_csv方法所需的关键字参数。
        :return: pandas.to_csv方法的返回值。
        """
        return self.__data.to_csv(**kwargs)

    def to_excel(self, excel_writer, **kwargs):
        """
        数据输出至excel格式文件。

        :param excel_writer: path-like, file-like, or ExcelWriter object
            File path or existing ExcelWriter.
        :param kwargs: pandas.to_excel方法所需的关键字参数。
        :return:
        """
        self.__data.to_excel(excel_writer, **kwargs)

    def to_dict(self, **kwargs):
        """
        数据转换为dict.

        :param kwargs:pandas.to_dict方法所需的关键字参数。
        :return:dict对象。
        """
        return self.__data.to_dict(**kwargs)
