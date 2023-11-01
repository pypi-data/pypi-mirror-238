# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Optional
from reytool.rdatabase import RDatabase as RRDatabase
from reytool.rfile import create_folder as reytool_create_folder


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.
    """


    def __init__(
        self,
        rrdatabase: Optional[RRDatabase] = None,
        receiver_no: int = 1,
        bandwidth: float = 5,
        timeout : Optional[float] = None
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        rrdatabase : RRDatabase instance.
            `None` : No attributes `rdatabase` and `database_use`.
            `RDatabase` : With attributes `rdatabase` and `database_use`.

        receiver_no : Number of receivers.
        bandwidth : Upload bandwidth, impact send interval, unit Mpbs.
        timeout : File receive timeout seconds.
            - `None` : Infinite time.
            - `float` : Use this value.
        """


        # Import.
        from .rclient import RClient
        from .rdatabase import RDatabase
        from .rlog import RLog
        from .rreceive import RReceive
        from .rsend import RSend


        # Set attribute.

        ## Instance.
        self.rclient = RClient(self)
        self.rreceive = RReceive(self, receiver_no, timeout)
        self.rsend = RSend(self, bandwidth)
        self.rlog = RLog(self)
        if rrdatabase is not None:
            self.rdatabase = RDatabase(self, rrdatabase)

        ## Method.
        self.receive = self.rreceive.receive
        self.receive_add_handler = self.rreceive.add_handler
        self.receive_start = self.rreceive.start
        self.receive_pause = self.rreceive.pause
        self.send = self.rsend.send
        self.send_start = self.rsend.start
        self.send_pause = self.rsend.pause
        if rrdatabase is not None:
            self.database_use = self.rdatabase.use_all

        # Create folder.
        self.create_folder()

        # Start.
        self.receive_start()
        self.send_start()
        self.rlog.add_print()
        self.rlog.add_file()


    @property
    def receive_started(self) -> bool:
        """
        Get receive start state.
        """

        # Get.
        started = self.rreceive.started

        return started


    @property
    def rsend_started(self) -> bool:
        """
        Get send start state.
        """

        # Get.
        started = self.rsend.started

        return started


    def create_folder(self) -> None:
        """
        Create project standard folders.
        """

        # Set parameter.
        paths = [
            ".\cache",
            ".\log"
        ]

        # Create.
        reytool_create_folder(paths)