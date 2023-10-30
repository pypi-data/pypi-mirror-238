# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-22 22:50:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Send methods.
"""


from typing import Tuple, Dict, Optional
from queue import Queue
from reytool.rsystem import rexc
from reytool.rtime import sleep
from reytool.rwrap import start_thread
from reytool.rnumber import randn
from reytool.rrequest import get_file_send_time

from .rclient import RClient


__all__ = (
    "RSend",
)


class RSend(object):
    """
    Rey's `send` type.
    """


    def __init__(
        self,
        rclient: RClient,
        bandwidth: float
    ) -> None:
        """
        Build `send` instance.

        Parameters
        ----------
        rclient : 'RClient' instance.
        bandwidth : Upload bandwidth, unit Mpbs.
        """

        # Set attribute.
        self.rclient = rclient
        self.bandwidth = bandwidth
        self.queue: Queue[Tuple[str, Dict]] = Queue()
        self.started: Optional[bool] = False

        # Start.
        self._create_sender()


    def get_interval(
        self,
        plan: Tuple[str, Dict],
        minimum: float = 0.8,
        maximum: float = 1.2,
    ) -> float:
        """
        Get message send `interval time`, unit seconds.

        Parameters
        ----------
        plan : Plan message type and message parameters.
            - `Parameter has key 'file' and is not None` : Calculate file send time, but not less than random seconds.
            - `Other` : Calculate random seconds.

        minimum : Random minimum seconds.
        maximum : Random maximum seconds.

        Returns
        -------
        Send interval seconds.
        """

        # Get parameters.
        type_, params = plan

        # Random.
        seconds = randn(minimum, maximum, precision=2)

        # File.
        if type_ == "file":
            file_seconds = get_file_send_time(params["file"], self.bandwidth)
            if file_seconds > seconds:
                seconds = file_seconds

        return seconds


    @start_thread
    def _create_sender(self) -> None:
        """
        Create `sender`, it will get message parameters from send queue and `send`.
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
            plan = self.queue.get()
            type_, params = plan
            if type_ == "text":
                self.rclient.send_text(**params, check=False)
            elif type_ == "file":
                self.rclient.send_file(**params, check=False)

            ## Interval.
            seconds = self.get_interval(plan)
            sleep(seconds)


    def start(self) -> None:
        """
        Start `sender`.
        """

        # Start.
        self.started = True


    def pause(self) -> None:
        """
        Pause `sender`.
        """

        # Pause.
        self.started = False


    def send(
        self,
        receiver: str,
        text: Optional[str] = None,
        ats: Optional[str] = None,
        file: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> None:
        """
        Queue add plan, waiting send `text` or `file` message.

        Parameters
        ----------
        receiver : WeChat user ID or room ID.
        text : Text message content. Conflict with parameter 'file'.
        ats : User ID to '@' of text message content, comma interval. Can only be use when parameter 'receiver' is room ID.
            - `None` : Not use '@'.
            - `str` : Use '@', parameter 'text' must have with ID same quantity '@' symbols.

        file : File message path. Conflict with parameter 'text'.
        timeout : Number of timeout seconds.

        Examples
        --------
        Send text.
        >>> receiver = 'uid_or_rid'
        >>> rclient.send(receiver, 'Hello!')

        Send text and '@'.
        >>> receiver = 'rid'
        >>> ats = ('uid1', 'uid2')
        >>> rclient.send(receiver, '@uname1 @uname2 Hello!', ats)

        Send file.
        >>> file = 'file_path'
        >>> rclient.send(receiver, file=file)
        """

        # Check.
        rexc.check_most_one(text, file)
        rexc.check_least_one(text, file)

        ## Text.
        if text is not None:
            if ats is not None:

                ### ID type.
                if "@chatroom" not in receiver:
                    raise ValueError("when using parameter 'ats', parameter 'receiver' must be room ID.")

                ### Count "@" symbol.
                comma_n = ats.count(",")
                at_n = text.count("@")
                if at_n < comma_n:
                    raise ValueError("when using parameter 'ats', parameter 'text' must have with ID same quantity '@' symbols")

        ## File.
        elif file is not None:

            ### Found.
            rexc.check_file_found(file)

        # Generate plan.

        ## Text.
        if text is not None:
            plan = (
                "text",
                {
                    "receiver": receiver,
                    "text": text,
                    "ats": ats
                }
            )

        elif file is not None:
            plan = (
                "file",
                {
                    "receiver": receiver,
                    "file": file
                }
            )

        # Add plan.
        self.queue.put(plan, timeout=timeout)


    __call__ = send


    def __del__(self) -> None:
        """
        Delete `send` instance handle.
        """

        # End.
        self.started = None