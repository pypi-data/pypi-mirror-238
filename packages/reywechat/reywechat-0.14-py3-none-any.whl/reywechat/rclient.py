# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Client methods.
"""


from __future__ import annotations
from typing import Any, Dict, Optional, Callable, overload
from functools import wraps as functools_wraps
from wcferry import Wcf, WxMsg
from reytool.rsystem import rexc


__all__ = (
    "RClient",
)


class RClient(object):
    """
    Rey's `client` type.
    """


    def __init__(self) -> None:
        """
        Build `client` instance.
        """

        # Start.
        self.client = self.start()


    def start(self) -> Wcf:
        """
        Start and login client.

        Returns
        -------
        Client instance.
        """

        # Start client.
        client = Wcf(debug=False)

        # Start receive.
        success = client.enable_receiving_msg()

        ## Check.
        if not success:
            raise AssertionError("start receiving message error")

        return client


    @overload
    def _check(func_or_code: Callable) -> Callable: ...

    @overload
    def _check(func_or_code: Any) -> Callable[[Callable], Callable]: ...

    def _check(func_or_code: Any) -> Callable[[Callable], Callable]:
        """
        Define decorator, add check client state and funtion call result, if check fail, throw exception.

        Parameters
        ----------
        func_or_value: Function or success value.
            - `Callable` : Decorate this function, add check client state, return decorated function.
            - `Any` : Define decorator, add check client state and funtion call result, return decorator.

        Returns
        -------
        Decorated function or decorator.
        """

        # Judge.
        judge = callable(func_or_code)
        if judge:
            func = func_or_code
            code = None
        else:
            func = None
            code = func_or_code


        # Define.
        def decorator(func_: Callable) -> Callable:
            """
            Decorator, add check client state and funtion call result.

            Parameters
            ----------
            func_ : Function.

            Returns
            -------
            Decorated function.
            """


            # Decorate.
            @functools_wraps(func_)
            def wrap(self: RClient, *args: Any, **kwargs: Any) -> Any:
                """
                Wrap.

                Parameters
                ----------
                args : Position parameters of function.
                kwargs : Keyword parameters of function.

                Returns
                -------
                Function return.
                """

                # Check.
                if not self.client.is_login():
                    raise AssertionError("client not started or logged in")

                # Execute.
                result = func_(self, *args, **kwargs)

                # Check.
                if (
                    code is not None
                    and result != code
                ):
                    text = "client call failed, now is %s" % repr(result)
                    raise AssertionError(text)

                return result


            return wrap


        # Decorator.
        if func is None:
            return decorator

        # Decorate.
        else:
            wrap = decorator(func)
            return wrap


    @overload
    def receive(
        self,
        timeout: Optional[float] = None
    ) -> WxMsg: ...

    @_check
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
        msg: WxMsg = self.client.msgQ.get(timeout=timeout)

        return msg


    @overload
    def send_text(
        self,
        receiver: str,
        text: str,
        ats: Optional[str] = None,
        check: bool = True
    ) -> int: ...

    @_check(0)
    def send_text(
        self,
        receiver: str,
        text: str,
        ats: Optional[str] = None,
        check: bool = True
    ) -> int:
        """
        Send text message.

        Parameters
        ----------
        receiver : WeChat user ID or room ID.
        text : Text message content.
        ats : User ID to '@' of text message content, comma interval. Can only be use when parameter 'receiver' is room ID.
            - `None` : Not use '@'.
            - `str` : Use '@', parameter 'text' must have with ID same quantity '@' symbols.

        check : Whether check parameters, not check can reduce calculations.

        Returns
        -------
        Send response code.
        """

        # Handle parameter.
        if ats is None:
            ats = ""

        # Check.
        elif check:

            ## ID type.
            if "@chatroom" not in receiver:
                raise ValueError("when using parameter 'ats', parameter 'receiver' must be room ID.")

            ## Count "@" symbol.
            comma_n = ats.count(",")
            at_n = text.count("@")
            if at_n < comma_n:
                raise ValueError("when using parameter 'ats', parameter 'text' must have with ID same quantity '@' symbols")

        # Send.
        response_code = self.client.send_text(text, receiver, ats)

        return response_code


    @overload
    def send_file(
        self,
        receiver: str,
        file: str,
        check: bool = True
    ) -> int: ...

    @_check(0)
    def send_file(
        self,
        receiver: str,
        file: str,
        check: bool = True
    ) -> int:
        """
        Send text message.

        Parameters
        ----------
        receiver : WeChat user ID or room ID.
        file : File message path.
        check : Whether check parameters, not check can reduce calculations.

        Returns
        -------
        Send response code.
        """

        # Check.
        if check:
            rexc.check_file_found(file)

        # Send.
        response_code = self.client.send_image(file, receiver)

        return response_code


    @_check
    def get_type_dict(self) -> Dict[int, str]:
        """
        Get message type dictionary.
        """

        # Get.
        type_dict = self.client.get_msg_types()

        return type_dict