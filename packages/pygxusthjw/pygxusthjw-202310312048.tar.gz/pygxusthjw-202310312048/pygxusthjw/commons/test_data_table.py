#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_data_table.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试data_table.py。
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

# 导包 =============================================================
import unittest
import numpy as np
import pandas as pd
from .data_table import DataTable


# ==================================================================
class TestDataTable(unittest.TestCase):
    """
    测试data_table.py。
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

    # noinspection PyUnresolvedReferences
    def test_constructor1(self):
        pd.set_option('display.max_columns', None)
        # 设置pandas显示所有行
        pd.set_option('display.max_rows', None)
        # 设置pandas显示所有字符
        pd.set_option('display.max_colwidth', None)

        table1 = DataTable()
        print(table1.shape)
        print(table1._DataTable__data)

        table2 = DataTable(1)
        print(table2.shape)
        print(table2._DataTable__data)

        table3 = DataTable(1, 2)
        print(table3.shape)
        print(table3._DataTable__data)

        table4 = DataTable(1, 2, [1])
        print(table4.shape)
        print(table4._DataTable__data)

        table5 = DataTable([1])
        print(table5.shape)
        print(table5._DataTable__data)

        table6 = DataTable([1, 2])
        print(table6.shape)
        print(table6._DataTable__data)

        table7 = DataTable([1], [1])
        print(table7.shape)
        print(table7._DataTable__data)

        table8 = DataTable([1], [1, 2])
        print(table8.shape)
        print(table8._DataTable__data)

        table9 = DataTable([1, 3, 5], [1, 2])
        print(table9.shape)
        print(table9._DataTable__data)

        table10 = DataTable([1, 3, 5], [1, 2], 2)
        print(table10.shape)
        print(table10._DataTable__data)

        table11 = DataTable(1, 3, 'a', [1, 3, 5], [1, 2], 2)
        print(table11.shape)
        print(table11._DataTable__data)

        table12 = DataTable(4, '5', [object], [1, 3, 5], [1, 2], 2)
        print(table12.shape)
        print(table12._DataTable__data)

        table13 = DataTable(1, 3, True, [1, 3, 5], [1, 2], 2)
        print(table13.shape)
        print(table13._DataTable__data)

        table14 = DataTable(4, '5', object, [1, 3, 5], [1, 2], 2)
        print(table14.shape)
        print(table14._DataTable__data)

        table15 = DataTable(4, '5', table14, [1, 3, 5], [1, 2], 2)
        print(table15.shape)
        print(table15._DataTable__data)

        table16 = DataTable(None)
        print(table16.shape)
        print(table16._DataTable__data)

    # noinspection PyUnresolvedReferences
    def test_constructor2(self):
        table1 = DataTable(1, col_names={0: 'one'})
        print(table1.shape)
        print(table1._DataTable__data)
        table2 = DataTable(1, col_names={0: 'one', 1: 'two'})
        print(table2.shape)
        print(table2._DataTable__data)

        table3 = DataTable(1, 2, 3, 4, col_names={0: 'one', 1: 'two'})
        print(table3.shape)
        print(table3._DataTable__data)

        table4 = DataTable(1, 2, 3, 4, col_names={1: 'one', 2: 'two'})
        print(table4.shape)
        print(table4._DataTable__data)

        table5 = DataTable(1, 2, 3, 4, col_names={1: 'one', 2: 'two', 3: 'three', 5: 'five'})
        print(table5.shape)
        print(table5._DataTable__data)

    # noinspection PyUnresolvedReferences
    def test_constructor3(self):
        table1 = DataTable(1,
                           col_names=['one'])
        print(table1.shape)
        print(table1._DataTable__data)

        table2 = DataTable(1,
                           col_names=['one', 'two'])
        print(table2.shape)
        print(table2._DataTable__data)

        table3 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two'])
        print(table3.shape)
        print(table3._DataTable__data)

        table4 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two', 'three'])
        print(table4.shape)
        print(table4._DataTable__data)

        table5 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two', 'three', 'five'])
        print(table5.shape)
        print(table5._DataTable__data)

    # noinspection PyUnresolvedReferences
    def test_add_col(self):
        table = DataTable()
        print(table.shape)
        print(table._DataTable__data)
        table.add_col(2, '0')
        print(table.shape)
        print(table._DataTable__data)

        table2 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two', 'three', 'five'])
        print(table2.shape)
        print(table2._DataTable__data)
        table2.add_col(2, '0')
        print(table2.shape)
        print(table2._DataTable__data)

        table3 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two', 'three', 'five'])
        print(table3.shape)
        print(table3._DataTable__data)
        table3.add_col([2, 0, 3, 4], '0')
        print(table3.shape)
        print(table3._DataTable__data)

        table4 = DataTable(1, 2, 3, 4,
                           col_names=['one', 'two', 'three', 'five'])
        print(table4.shape)
        print(table4._DataTable__data)
        table4.add_col([2, 0, 3, 4])
        table4.add_col([2, 0, 3, 4])
        table4.add_col([2, 0, 3, 4])
        table4.add_col([2, 0, 3, 4])
        print(table4.shape)
        print(table4._DataTable__data)

    def test_get_col(self):
        table3 = DataTable(1, [1, 2], None, (4, 5, 6, 7), np.arange(20),
                           col_names=['one', 'two', 'three', 'five'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})

        print(table3.get_col('one'))
        print(table3.get_col('two'))
        print(table3.get_col('three'))
        print(table3.get_col('five'))
        print(table3.get_col('col_4'))

        print(table3.get_col(0))
        print(table3.get_col(1))
        print(table3.get_col(2))
        print(table3.get_col(3))
        print(table3.get_col(4))


if __name__ == '__main__':
    unittest.main()
