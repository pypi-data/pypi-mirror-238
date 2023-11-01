#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        path_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为"路径"提供辅助方法或类。
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


# ==================================================================

def join_file_path(path: str, file_base_name: str,
                   file_type: str = '', suffix="_副本") -> str:
    """
    将文件路径、文件名和文件类型结合为完整的文件路径。

    如果文件的完整路径下已存在指定的文件，则在文件名后加“_副本”。

    该方法并不实际创建文件，只是链接文件路径。

    :param path: 路径。
    :param file_base_name: 文件名（不含扩展名）。
    :param file_type: 文件类型（即文件的扩展名，含“.”），如果不包含“.”，则自动添加“.”。
    :param suffix: 后缀。
    :return: 完整的文件路径。
    """
    if not file_type.startswith("."):
        file_type = ".{}".format(file_type.strip())
    path_file = path + os.sep + file_base_name + file_type
    if os.path.exists(path_file):
        return join_file_path(path, file_base_name + suffix, file_type)
    else:
        return path_file


def sep_file_path(file, with_dot_in_ext=True):
    """
    获取指定文件路径的文件名和父目录。

    :param file: 文件完整路径。
    :param with_dot_in_ext: 指定返回的文件扩展名中是否包含“.”，如果为True，则包含，否则不包含。
    :return: (文件父目录, 文件基名，文件扩展名)
    """
    filepath, temp_file_name = os.path.split(file)
    filename, file_ext = os.path.splitext(temp_file_name)
    if not with_dot_in_ext:
        file_ext = file_ext.replace(".", " ").strip()
    return filepath, filename, file_ext
