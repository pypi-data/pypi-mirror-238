# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Optional
from reytool.rdatabase import RDatabase

from .rclient import RClient
from .rdatabase import RDatabase
from .rreceive import RReceive
from .rsend import RSend


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.
    """


    def __init__(
        self,
        rdatabase: Optional[RDatabase] = None,
        bandwidth: float = 5
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        rdatabase : RDatabase instance.
            `None` : No attributes `rdatabase` and `database_use`.
            `RDatabase` : With attributes `rdatabase` and `database_use`.

        bandwidth : Upload bandwidth, unit Mpbs.
        """

        # Set attribute.

        ## Instance.
        self.rclient = RClient()
        self.rreceive = RReceive(self.rclient)
        self.rsend = RSend(self.rclient, bandwidth)
        if rdatabase is not None:
            self.rdatabase = RDatabase(
                self.rclient,
                self.rreceive,
                self.rsend,
                rdatabase
            )

        ## Method.
        self.receive = self.rreceive.receive
        self.receive_add_handler = self.rreceive.add_handler
        self.receive_start = self.rreceive.start
        self.receive_pause = self.rreceive.pause
        self.send = self.rsend.send
        self.send_start = self.rsend.start
        self.send_pause = self.rsend.pause
        if rdatabase is not None:
            self.database_use = self.rdatabase.use

        # Start.
        self.receive_start()
        self.send_start()


    @property
    def receive_started(self) -> bool:
        """
        Get receive `start state`.
        """

        # Get.
        started = self.rreceive.started

        return started


    @property
    def rsend_started(self) -> bool:
        """
        Get send `start state`.
        """

        # Get.
        started = self.rsend.started

        return started