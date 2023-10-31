# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from typing import Optional
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
        rrdatabase: RRDatabase
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rclient : RClient instance.
        rreceive : RReceive instance.
        rsend : RSend instance.
        rrdatabase : RRDatabase instance.
        """

        # Set attribute.
        self.rclient = rclient
        self.rreceive = rreceive
        self.rsend = rsend
        self.rrdatabase = rrdatabase


    def update_message_type(self) -> None:
        """
        Update table `message_type`.
        """

        # Get data.
        type_dict = self.rclient.get_type_dict()
        data = [
            {
                "type": type_,
                "description": description
            }
            for type_, description in type_dict.items()
        ]

        # Insert and update.
        self.rrdatabase.execute_insert(
            ("wechat", "message_type"),
            data,
            "update"
        )


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
                        "type_": "char(20)",
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
                        "type_": "mediumint unsigned",
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
            },

            ### "message_type".
            {
                "path": ("wechat", "message_type"),
                "fields": [
                    {
                        "name": "type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type.",
                    },
                    {
                        "name": "description",
                        "type_": "varchar(200)",
                        "constraint": "NOT NULL",
                        "comment": "Message type description.",
                    }
                ],
                "primary": "type",
                "comment": "Message type table."
            },
        ]

        # Build.
        self.rrdatabase.build(databases, tables)

        ## File.
        self.rrdatabase.file()

        # Insert.
        self.update_message_type()


    def upload_file(
        self,
        message: WxMsg
    ) -> int:
        """
        Upload file.

        Parameters
        ----------
        message : Message instance.

        Returns
        -------
        File ID.
        """

        # Get parameter.
        file_path: Optional[str] = message.file

        # Break.
        if file_path is None: return

        # Upload.
        file_id = self.rrdatabase.file.upload(file_path, uploader="WeChat")

        return file_id


    def use_message_receive(self) -> None:
        """
        Write message parameters to table `message_receive`.
        """


        # Define.
        def method(message: WxMsg) -> None:
            """
            Message handle methods.

            Parameters
            ----------
            message : Message instance.
            """

            # Upload file.
            file_id = self.upload_file(message)

            # Generate data.
            data = {
                "uuid": message.id,
                "room": message.roomid,
                "sender": message.sender,
                "type": message.type,
                "content": message.content,
                "xml": message.xml,
                "file": file_id,
                "receiver": self.rclient.client.self_wxid
            }
            kwdata = {
                "time": ":NOW()"
            }

            self.rrdatabase.execute_insert(
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