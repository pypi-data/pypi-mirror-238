# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from wcferry import WxMsg
from reytool.rdatabase import RDatabase as RRDatabase

from .rclient import RClient
from .rreceive import RReceive
from .rsend import RSend


__all__ = (
    "RDatabase",
)


class RDatabase(object):
    """
    Rey's `database` type.
    """


    def __init__(
        self,
        rclient: RClient,
        rreceive: RReceive,
        rsend: RSend,
        rrengine: RRDatabase
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rclient : RClient instance.
        rreceive : RReceive instance.
        rsend : RSend instance.
        rrengine : RRDatabase instance.
        """

        # Set attribute.
        self.rclient = rclient
        self.rreceive = rreceive
        self.rsend = rsend
        self.rrengine = rrengine


    def build(self) -> None:
        """
        `Check` and `build` all standard databases and tables.
        Include database `wechat` and table `receive_message`.
        """

        # Set parameter.

        ## Database.
        databases = [
            {
                "database": "wechat"
            }
        ]

        ## Table.
        tables = [

            ### "receive_message".
            {
                "path": ("wechat", "receive_message"),
                "fields": [
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "Message receive time.",
                    },
                    {
                        "name": "id",
                        "type_": "bigint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message ID.",
                    },
                    {
                        "name": "room_id",
                        "type_": "varchar(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message room ID.",
                    },
                    {
                        "name": "receiver",
                        "type_": "varchar(24)",
                        "constraint": "NOT NULL",
                        "comment": "Message receiver ID.",
                    },
                    {
                        "name": "sender",
                        "type_": "varchar(24)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message sender ID.",
                    },
                    {
                        "name": "type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type.",
                    },
                    {
                        "name": "content",
                        "type_": "text",
                        "constraint": "NOT NULL",
                        "comment": "Message content.",
                    },
                    {
                        "name": "xml",
                        "type_": "text",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message XML content.",
                    },
                    {
                        "name": "file",
                        "type_": "varchar(1000)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message file path.",
                    }
                ],
                "primary": "id",
                "comment": "Receive message table."
            }
        ]

        # Build.
        self.rrengine.build(databases, tables)


    def use_receive_message(self) -> None:
        """
        Write message parameters to table `receive_message`.
        """


        # Define.
        def method(msg: WxMsg) -> None:

            # Generate data.
            data = {
                "id": msg.id,
                "room_id": msg.roomid,
                "receiver": self.rclient.client.self_wxid,
                "sender": msg.sender,
                "type": msg.type,
                "content": msg.content,
                "xml": msg.xml,
                "file": msg.extra
            }
            kwdata = {
                "time": ":NOW()"
            }

            self.rrengine.execute_insert(
                ("wechat", "receive_message"),
                data,
                **kwdata
            )

        # Add handler.
        self.rreceive.add_handler(method)


    def use(self) -> None:
        """
        Use all database tables.
        Include database `wechat` and table `receive_message`.
        """

        # Check and build.
        self.build()

        # Use.

        ## "receive_message".
        self.use_receive_message()


    __call__ = use