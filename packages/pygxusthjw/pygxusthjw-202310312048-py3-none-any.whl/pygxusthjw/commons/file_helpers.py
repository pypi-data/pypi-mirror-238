#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        file_helpers.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 提供“文件”相关的辅助类和方法。
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
import inspect
import os.path
import sys
from typing import Optional
import chardet


# ==================================================================
# noinspection PyBroadException
def get_file_encoding_chardet(file_path):
    """
    利用chardet库获取文件的编码。

    :param file_path: 文件的完整路径。
    :return: 文件的编码。
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
                return encoding
        except Exception:
            return None
    else:
        return None


def file_info(directory_path: str, base_name: str,
              ext_name: Optional[str] = None,
              encoding: Optional[str] = None,
              **kwargs):
    """
    构造文件信息对象。

    :param directory_path: 文件所在目录的路径。
    :param base_name: 文件基名。
    :param ext_name: 文件扩展名（不含`.`），缺省为None。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileInfo对象。
    """
    return FileInfo(directory_path, base_name, ext_name, encoding,
                    **kwargs)


def get_file_info(file_path: str, encoding: Optional[str] = None,
                  **kwargs):
    """
    获取文件信息对象。

    :param file_path: 文件的完整路径。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileInfo对象。
    """
    directory_path, file_name = os.path.split(file_path)
    base_name, ext_name = os.path.splitext(file_name)
    return FileInfo(directory_path, base_name, ext_name, encoding,
                    **kwargs)


def get_file_info_of_module(mod_name):
    """
    利用inspect库获取指定模块名的文件信息。

    :param mod_name: 指定的模块名。
    :return: FileInfo对象。
    """
    file_path = inspect.getfile(sys.modules[mod_name])
    return get_file_info(file_path)


class FileInfo(object):
    """
    类`FileInfo`用于承载”文件信息“。
    """

    def __init__(self, directory_path: str, base_name: str,
                 ext_name: Optional[str] = None,
                 encoding: Optional[str] = None,
                 **kwargs):
        """
        类`FileInfo`的初始化方法。

        :param directory_path: 文件所在目录的路径。
        :param base_name: 文件基名。
        :param ext_name: 文件扩展名（不含`.`），缺省为None。
        :param encoding: 文件编码，缺省为None。
        :param kwargs: 有关文件的其他信息，将被转化为对象属性。
        """
        self.__directory_path = directory_path
        self.__base_name = base_name
        self.__ext_name = ext_name

        # 如果文件扩展名包含点，则将点删除。
        if self.__ext_name.startswith('.'):
            self.__ext_name = self.__ext_name[1:]

        # 构建文件名。
        if ext_name is not None:
            self.__name = "{}.{}".format(
                self.__base_name,
                self.__ext_name)
        else:
            self.__name = self.__base_name

        # 构建文件的路径。
        self.__path = os.path.join(self.__directory_path,
                                   self.__name)

        # 尝试获取文件的编码。
        self.__encoding = encoding
        if self.__encoding is None:
            self.__encoding = get_file_encoding_chardet(self.__path)

        # 其他关键字参数被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def directory_path(self) -> str:
        """
        获取文件所在目录的路径。

        :return: 文件所在目录的路径。
        """
        return self.__directory_path

    @property
    def base_name(self) -> str:
        """
        获取文件基名。

        :return: 文件基名。
        """
        return self.__base_name

    @property
    def ext_name(self) -> Optional[str]:
        """
        获取文件扩展名（不含`.`）。

        :return: 文件扩展名（不含`.`）。
        """
        return self.__ext_name

    @property
    def name(self) -> str:
        """
        获取文件名。

        :return: 文件名。
        """
        return self.__name

    @property
    def path(self) -> str:
        """
        获取文件的路径。

        :return: 文件的路径。
        """
        return self.__path

    @property
    def encoding(self) -> Optional[str]:
        """
        获取文件编码。

        :return: 文件编码。
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, new_encoding: str):
        """
        设置文件编码。

        :param new_encoding: 新的文件编码。
        :return: None
        """
        self.__encoding = new_encoding

    def make_directory(self):
        """
        创建文件目录

        :return: None
        """
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)

    def make_file(self):
        """
        创建文件。

        :return: None
        """
        self.make_directory()
        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def __eq__(self, other):
        """
        重载`==`操作符。

        :param other: 另一个FileInfo对象。
        :return: 相等返回True，否则返回False。
        """
        if isinstance(other, FileInfo):
            if self.path == other.path:
                return True
        else:
            return False

    def __ne__(self, other):
        """
        重载`!=`操作符。

        :param other: 另一个FileInfo对象。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        获取对象的hash码。

        :return: 对象的hash码。
        """
        result: int = 1
        for arg in (self.directory_path, self.base_name, self.ext_name):
            result = 31 * result + (0 if arg is None else hash(arg))

        return result

    def __str__(self):
        """
        获取对象字符串。

        :return:对象字符串。
        """
        return self.path

    def __repr__(self):
        """
        获取对象的文本式。

        :return:对象的文本式。
        """
        res_dict = dict()
        for key in self.__dict__:
            if key.startswith("_FileInfo__"):
                res_dict[key.removeprefix("_FileInfo__")] = self.__dict__[key]
            else:
                res_dict[key] = self.__dict__[key]
        return "FileInfo{}".format(res_dict)
