# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-19 11:33:45
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from os.path import abspath as os_abspath
from logging import getLogger
from reytool.rlog import RLog as RRLog

from .rwechat import RWeChat


__all__ = (
    "RLog",
)


class RLog(object):
    """
    Rey's `log` type.
    """


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `log` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        """

        # Set attribute.
        self.rwechat = rwechat

        # Instance.
        self.log = RRLog("WeChat")


    def add_print(self) -> None:
        """
        Add print handler.
        """

        # Add.
        self.log.add_print()


    def add_file(self) -> None:
        """
        Add file handler.
        """

        # Set parameter.
        file_path = os_abspath(r".\logs\WeChat")

        # Add.
        self.log.add_file(file_path, time="m")