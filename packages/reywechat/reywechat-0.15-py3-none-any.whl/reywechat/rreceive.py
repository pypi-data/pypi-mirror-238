# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-26 11:18:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Receive methods.
"""


from __future__ import annotations
from typing import Any, List, Optional, Callable
from os.path import (
    abspath as os_abspath,
    splitext as os_splitext,
    exists as os_exists,
    join as os_join
)
from threading import Thread
from queue import Queue
from wcferry import WxMsg
from reytool.rfile import search_file
from reytool.rtime import sleep
from reytool.rwrap import start_thread, wait

from .rclient import RClient


__all__ = (
    "RReceive",
)


class RReceive(object):
    """
    Rey's `receive` type.
    """


    def __init__(
        self,
        rclient: RClient,
        receivers: int,
        timeout : Optional[float]
    ) -> None:
        """
        Build `receive` instance.

        Parameters
        ----------
        rclient : 'RClient' instance.
        receivers : Number of receivers.
        timeout : File receive timeout seconds.
            - `None` : Infinite time.
            - `float` : Use this value.
        """

        # Set attribute.
        self.rclient = rclient
        self.timeout = timeout
        self.handlers: List[Callable[[WxMsg], Any]] = []
        self.queue: Queue[WxMsg] = Queue()
        self.started: Optional[bool] = False
        self.cache_path = os_abspath("cache")

        # Receiver.
        self.receivers: List[Thread] = [
            self._create_receiver()
            for n in range(receivers)
        ]

        # Add handler.
        self.handlers.append(self._file_handler)


    @start_thread
    def _create_receiver(self) -> None:
        """
        Create receiver, it will get message parameters from receive queue and handle.
        """

        # Loop.
        while True:

            ## Pause.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Start.
            message: WxMsg = self.rclient.client.msgQ.get()
            for handler in self.handlers:
                handler(message)

            ## Put.
            self.queue.put(message)


    def _file_handler(self, message: WxMsg) -> None:
        """
        File handler, decrypt image, and add file path attribute to message instance.

        Parameters
        ----------
        message : Message instance.
        """

        # Break.
        if message.extra in ("", None):
            message.file: Optional[str] = None
            return

        # Wait file.
        wait(
            os_exists,
            message.extra,
            _timeout=self.timeout
        )

        # Image.
        _, suffix = os_splitext(message.extra)
        if suffix == ".dat":
            file_name = str(message.id)
            save_path = os_join(self.cache_path, file_name)

            ## Decrypt.
            success = self.rclient.client.decrypt_image(message.extra, save_path)
            if not success:
                raise AssertionError("image file decrypt fail")

            ## Get path.
            pattern = "^%s." % file_name
            file_path = search_file(pattern, self.cache_path)

        # Other.
        else:
            file_path = message.extra

        # Set attribute
        message.file: Optional[str] = file_path


    def start(self) -> None:
        """
        Start receiver.
        """

        # Start.
        self.started = True


    def pause(self) -> None:
        """
        Pause receiver.
        """

        # Pause.
        self.started = False


    def add_handler(
        self,
        method: Callable[[WxMsg], Any]
    ) -> None:
        """
        Add method message handler.

        Parameters
        ----------
        method : Handler method. The parameter is the `WxMsg` instance.
        """

        # Add.
        self.handlers.append(method)


    def receive(
        self,
        timeout: Optional[float] = None
    ) -> WxMsg:
        """
        Receive one message.

        Parameters
        ----------
        timeout : Number of timeout seconds.

        Returns
        -------
        Message instance.
        """

        # Receive.
        message: WxMsg = self.queue.get(timeout=timeout)

        return message


    def __del__(self) -> None:
        """
        Delete receiver instance handle.
        """

        # End.
        self.started = None