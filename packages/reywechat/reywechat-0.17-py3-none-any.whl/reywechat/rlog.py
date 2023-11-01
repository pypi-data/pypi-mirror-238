# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-19 11:33:45
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from os import mkdir as os_mkdir
from os.path import (
    abspath as os_abspath,
    exists as os_exists
)
from logging import getLogger
from reytool.rlog import RLog as RRLog

from .rwechat import RWeChat


__all__ = (
    "RLog",
    "rlog"
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

        # Pause "WCF".
        self._pause_log_wcf()


    def _pause_log_wcf(self) -> None:
        """
        Pause `WCF` logger of `wcferry` module.
        """

        # Get parameter.
        wcf = getLogger("WCF")

        # Pause.
        wcf.setLevel(100)


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
        file_path = os_abspath(r"\log\WeChat")

        # Add.
        self.log.add_file(file_path, time="m")