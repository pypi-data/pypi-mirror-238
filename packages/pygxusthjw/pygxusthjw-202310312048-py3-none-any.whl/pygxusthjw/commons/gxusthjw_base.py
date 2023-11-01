#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        gxusthjw_base.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 提供基(base)类型。
#                   Outer Parameters: xxxxxxx
# Class List:       Author -- 表征“作者”，用于承载"作者"信息。
#                   Version -- 表征”版本“，用于承载"版本"信息。
#                   Copyright -- 表征”版权声明“，用于承载"版权"信息。
#                   Base -- 表征“基类型”，可作为所有类型的父类。
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
# ------------------------------------------------------------------
# 导包 =============================================================
from typing import Tuple, Optional


# ==================================================================

class Author(object):
    """
    类`Author`表征“作者”，用于承载作者信息。
    """

    def __init__(self, name: Optional[str] = "Jiwei Huang",
                 emails: Optional[Tuple[str, ...]] = ("jiweihuang@vip.163.com",
                                                      "jiweihuang@yeah.net",
                                                      "huangjiwei@gxust.edu.cn"),
                 organizations: Optional[Tuple[str, ...]] =
                 ("Guangxi University of Science and Technology",)):
        """
        类`Author`的初始化方法。

        :param name: 作者的姓名。
        :param emails: 作者的E-mail地址，可以指定多个。
        :param organizations: 作者所属的组织，可以指定多个。
        """
        if name is None:
            self.__name: str = "Jiwei Huang"
        else:
            self.__name: str = name

        if emails is None:
            self.__emails: Tuple[str, ...] = (
                "jiweihuang@vip.163.com",
                "jiweihuang@yeah.net",
                "huangjiwei@gxust.edu.cn")
        else:
            self.__emails: Tuple[str, ...] = emails

        if organizations is None:
            self.__organizations: Tuple[str, ...] = (
                "Guangxi University of Science and Technology",)
        else:
            self.__organizations: Tuple[str, ...] = organizations

    @property
    def name(self) -> str:
        """
        获取作者的姓名。

        :return: 作者的姓名。
        """
        return self.__name

    @property
    def emails(self) -> Tuple[str, ...]:
        """
        获取作者的E-mail地址。

        :return: 作者的E-mail地址，可能有多个。
        """
        return self.__emails

    @property
    def organizations(self) -> Tuple[str, ...]:
        """
        获取作者所属的组织。

        :return: 作者所属的组织，可能有多个。
        """
        return self.__organizations

    def __eq__(self, other_obj: object) -> bool:
        """
        比较与另一个对象的相等性。

        :param other_obj: 另一个对象。
        :return: 相等返回True，否则返回False。
        """
        if not isinstance(other_obj, Author):
            return False
        return self.name == other_obj.name and \
            self.emails == other_obj.emails and \
            self.organizations == other_obj.organizations

    def __hash__(self) -> int:
        """
        获取对象的hashcode码。

        :return: 对象的hashcode码。
        """
        result: int = 1
        for arg in (self.name, self.emails,
                    self.organizations):
            result = 31 * result + (0 if arg is None else hash(arg))
        return result

    def __str__(self) -> str:
        """
        获取作者字符串。

        :return: 作者字符串。
        """
        return "Author{{name={},emails={}," \
               "organizations={}}}".format(self.name,
                                           self.emails,
                                           self.organizations)

    def __repr__(self) -> str:
        """
        获取作者对象字符串。

        :return: 作者对象字符串。
        """
        return "{{{},{},{}}}".format(self.name,
                                     self.emails,
                                     self.organizations)


class Version(object):
    """
    类`Version`表征”版本“，用于承载版本信息。
    """

    def __init__(self, major: int = 1,
                 minor: int = 0,
                 build: int = 0,
                 revision: int = 0):
        """
        类`Version`的初始化方法。

        :param major:  主版本号。
        :param minor:  次版本号。
        :param build:  构建版本号。
        :param revision:  修订版本号。
        """
        if major < 0:
            raise ValueError("Expected major >= 0, but got {}.".format(major))
        if minor < 0:
            raise ValueError("Expected minor >= 0, but got {}.".format(minor))
        if build < 0:
            raise ValueError("Expected build >= 0, but got {}.".format(build))
        if revision < 0:
            raise ValueError("Expected revision >= 0, but got {}.".format(revision))

        if major == 0 and minor == 0 and build == 0 and revision == 0:
            raise ValueError("major,minor,build and revision can not all be equal to 0.")

        self.__major: int = major
        self.__minor: int = minor
        self.__build: int = build
        self.__revision: int = revision

    @property
    def major(self) -> int:
        """
        获取主版本号。

        :return: 主版本号。
        """
        return self.__major

    @property
    def minor(self) -> int:
        """
        获取次版本号。

        :return: 次版本号。
        """
        return self.__minor

    @property
    def build(self) -> int:
        """
        获取构建版本号。

        :return: 构建版本号。
        """
        return self.__build

    @property
    def revision(self) -> int:
        """
        获取修订版本号。

        :return: 修订版本号。
        """
        return self.__revision

    def __eq__(self, other_obj: object) -> bool:
        """
        比较与另一个对象的相等性。

        :param other_obj: 另一个对象。
        :return: 相等返回True，否则返回False。
        """
        if not isinstance(other_obj, Version):
            return False
        return self.major == other_obj.major and \
            self.minor == other_obj.minor and \
            self.build == other_obj.build and \
            self.revision == other_obj.revision

    def __hash__(self):
        """
        获取对象的hashcode码。

        :return: 对象的hashcode码。
        """
        result: int = 1
        for arg in (self.major, self.minor,
                    self.build, self.revision):
            result = 31 * result + (0 if arg is None else hash(arg))
        return result

    def __str__(self) -> str:
        """
        获取版本字符串。

        :return: 版本字符串。
        """
        return "Version{{major={},minor={}," \
               "build={},revision={}}}".format(self.major,
                                               self.minor,
                                               self.build,
                                               self.revision)

    def __repr__(self) -> str:
        """
        获取版本对象字符串。

        :return: 版本对象字符串。
        """
        return "({},{},{},{})".format(self.major,
                                      self.minor,
                                      self.build,
                                      self.revision)


class Copyright(object):
    """
    类`Copyright`表征”版权声明“，用于承载版权信息。
    """

    def __init__(self, statement: Optional[str] = None,
                 agreements: Optional[Tuple[str, ...]] = None):
        """
        类`Copyright`的初始化方法。

        :param statement: 版权声明，缺省值为：
                          ”Copyright (c) 2016-2023, Jiwei Huang. All Rights Reserved.“。
        :type statement: str
        :param agreements: 版权协议（例如：BSD, Apache, GPL, LGPL, MIT等），缺省值为：()。
        :type agreements: Tuple[str, ...]
        """
        if statement is None:
            self.__statement = "Copyright (c) 2016-2023, Jiwei Huang. All Rights Reserved."
        else:
            self.__statement = statement

        if agreements is None:
            self.__agreements = ()
        else:
            self.__agreements = agreements

    @property
    def statement(self) -> str:
        """
        获取版权声明。

        :return: 版权声明。
        """
        return self.__statement

    @property
    def agreements(self) -> Tuple[str, ...]:
        """
        获取版权协议。

        :return: 版权协议。
        """
        return self.__agreements

    def __eq__(self, other_obj: object) -> bool:
        """
        比较与另一个对象的相等性。

        :param other_obj: 另一个对象。
        :return: 相等返回True，否则返回False。
        """
        if not isinstance(other_obj, Copyright):
            return False
        return self.statement == other_obj.statement and \
            self.agreements == other_obj.agreements

    def __hash__(self):
        """
        获取对象的hashcode码。

        :return: 对象的hashcode码。
        """
        result: int = 1
        for arg in (self.statement, self.agreements):
            result = 31 * result + (0 if arg is None else hash(arg))
        return result

    def __str__(self) -> str:
        """
        获取版权字符串。

        :return: 版权字符串。
        """
        return "Copyright{{statement={},agreements={}}}".format(
            self.statement, self.agreements)

    def __repr__(self) -> str:
        """
        获取版权对象字符串。

        :return: 版权对象字符串。
        """
        return "({},{})".format(self.statement,
                                self.agreements)


class Base(object):
    """
    类`Base`表征“基类型”，可作为所有类型的父类。
    """

    def __init__(self, author: Optional[Author] = None,
                 version: Optional[Version] = None,
                 copyright_info: Optional[Copyright] = None):
        """
        类`Base`的初始化方法。

        :param author: 类的作者。
        :type author: Author
        :param version: 类的版本。
        :type version:Version
        :param copyright_info: 类的版权。
        :type copyright_info:Copyright
        """
        if author is None:
            self.__author = Author(
                "Jiwei Huang",
                ("jiweihuang@vip.163.com",
                 "jiweihuang@yeah.net",
                 "huangjiwei@gxust.edu.cn"),
                (
                    "Guangxi University of Science and Technology",)
            )
        else:
            self.__author = author

        if version is None:
            self.__version = Version(1, 0, 0, 0)
        else:
            self.__version = version

        if copyright_info is None:
            self.__copyright = Copyright(
                "Copyright (c) 2016-2023, Jiwei Huang. All Rights Reserved.",
                ())
        else:
            self.__copyright = copyright_info

        if not isinstance(self.__author, Author):
            raise TypeError("Expected the type of author is Author, "
                            "but got {}.".format(type(self.__author)))

        if not isinstance(self.__version, Version):
            raise TypeError("Expected the type of version is Version, "
                            "but got {}.".format(type(self.__version)))

        if not isinstance(self.__copyright, Copyright):
            raise TypeError("Expected the type of copyright_info is Copyright, "
                            "but got {}.".format(type(self.__copyright)))

    @property
    def author(self) -> Author:
        """
        获取类的的作者。

        :rtype: Author
        :return: 类的的作者。
        """
        return self.__author

    @property
    def version(self) -> Version:
        """
        获取类的版本。

        :rtype: Version
        :return: 类的版本。
        """
        return self.__version

    @property
    def copyright(self) -> Copyright:
        """
        获取类的版权。

        :rtype: Copyright
        :return: 类的版权。
        """
        return self.__copyright

    def __eq__(self, other_obj: object) -> bool:
        """
        比较与另一个对象的相等性。

        :param other_obj: 另一个对象。
        :return: 相等返回True，否则返回False。
        """
        if not isinstance(other_obj, Base):
            return False
        return self.author == other_obj.author and \
            self.version == other_obj.version and \
            self.copyright == other_obj.copyright

    def __hash__(self):
        """
        获取对象的hashcode码。

        :return: 对象的hashcode码。
        """
        result: int = 1
        for arg in (self.author, self.version,
                    self.copyright):
            result = 31 * result + (0 if arg is None else hash(arg))
        return result

    def __str__(self) -> str:
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return "Base{{name={},version={}," \
               "copyright={}}}".format(self.author,
                                       self.version,
                                       self.copyright)

    def __repr__(self) -> str:
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        return "{{{},{},{}}}".format(self.author,
                                     self.version,
                                     self.copyright)
