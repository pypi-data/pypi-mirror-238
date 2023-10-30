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
from queue import Queue
from wcferry import WxMsg
from reytool.rtime import sleep
from reytool.rwrap import start_thread

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
        rclient: RClient
    ) -> None:
        """
        Build `receive` instance.

        Parameters
        ----------
        rclient : 'RClient' instance.
        """

        # Set attribute.
        self.rclient = rclient
        self.handlers: List[Callable[[WxMsg], Any]] = []
        self.queue: Queue[WxMsg] = Queue()
        self.started: Optional[bool] = False

        # Start.
        self._create_receiver()


    @start_thread
    def _create_receiver(self) -> None:
        """
        Create `receiver`, it will get message parameters from receive queue and `handle`.
        """

        # Loop.
        while True:

            ## End.
            if self.started is None:
                break

            ## Pause.
            elif not self.started:
                sleep(0.1)
                continue

            ## Start.
            msg: WxMsg = self.rclient.client.msgQ.get()
            for handler in self.handlers:
                handler(msg)

            ## Put.
            self.queue.put(msg)


    def start(self) -> None:
        """
        Start `receiver`.
        """

        # Start.
        self.started = True


    def pause(self) -> None:
        """
        Pause `receiver`.
        """

        # Pause.
        self.started = False


    def add_handler(
        self,
        method: Callable[[WxMsg], Any]
    ) -> None:
        """
        Add `method` message handler.

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
        msg: WxMsg = self.queue.get(timeout=timeout)

        return msg


    def __del__(self) -> None:
        """
        Delete `receiver` instance handle.
        """

        # End.
        self.started = None