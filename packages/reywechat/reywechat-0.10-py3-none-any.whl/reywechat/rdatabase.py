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
        Check and build all standard databases and tables.
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

            ### "message_receive".
            {
                "path": ("wechat", "message_receive"),
                "fields": [
                    {
                        "name": "id",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL AUTO_INCREMENT",
                        "comment": "Message ID.",
                    },
                    {
                        "name": "uuid",
                        "type_": "bigint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message UUID.",
                    },
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "Message receive time.",
                    },
                    {
                        "name": "room",
                        "type_": "varchar(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message room ID.",
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
                        "comment": "Message file ID.",
                    },
                    {
                        "name": "receiver",
                        "type_": "varchar(24)",
                        "constraint": "NOT NULL",
                        "comment": "Message receiver ID.",
                    }
                ],
                "primary": "id",
                "comment": "Message receive table."
            }
        ]

        # Build.
        self.rrengine.build(databases, tables)

        ## File.
        self.rrengine.file.build()


    def upload_file(
        self,
        msg: WxMsg
    ) -> int:
        """
        Upload file.

        Parameters
        ----------
        msg : Message instance.

        Returns
        -------
        File ID.
        """

        return None


    def use_message_receive(self) -> None:
        """
        Write message parameters to table `message_receive`.
        """


        # Define.
        def method(msg: WxMsg) -> None:
            """
            Message handle methods.

            Parameters
            ----------
            msg : Message instance.
            """

            # Upload file.
            file_id = self.upload_file(msg)

            # Generate data.
            data = {
                "uuid": msg.id,
                "room": msg.roomid,
                "sender": msg.sender,
                "type": msg.type,
                "content": msg.content,
                "xml": msg.xml,
                "file": file_id,
                "receiver": self.rclient.client.self_wxid
            }
            kwdata = {
                "time": ":NOW()"
            }

            self.rrengine.execute_insert(
                ("wechat", "message_receive"),
                data,
                **kwdata
            )

        # Add handler.
        self.rreceive.add_handler(method)


    def use(self) -> None:
        """
        Use all database tables.
        """

        # Check and build.
        self.build()

        # Use.

        ## "message_receive".
        self.use_message_receive()


    __call__ = use