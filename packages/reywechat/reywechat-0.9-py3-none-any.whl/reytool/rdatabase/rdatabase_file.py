# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-29 20:01:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database file methods.
"""


from typing import Union, Optional
from os.path import (
    basename as os_basename,
    isdir as os_isdir,
    join as os_join
)

from .rdatabase import RDatabase, RDBConnection
from ..rfile import read_file, write_file, get_md5


class RDBFile(object):
    """
    Rey's `database file` type.
    """


    def __init__(
        self,
        rdatabase: Union[RDatabase, RDBConnection]
    ) -> None:
        """
        Build `database file` instance.

        Parameters
        ----------
        rdatabase : RDatabase or RDBConnection instance.
        """

        # Set attribute.
        self.rdatabase = rdatabase


    def build(self) -> None:
        """
        `Check` and `build` all standard databases and tables.
        Include database `file` and table `information`, `data`, `data_big`.
        """

        # Set parameter.

        ## Database.
        databases = [
            {
                "database": "file"
            }
        ]

        ## Table.
        tables = [

            ### "information".
            {
                "path": ("file", "information"),
                "fields": [
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "File upload time.",
                    },
                    {
                        "name": "id",
                        "type_": "mediumint unsigned",
                        "constraint": "NOT NULL AUTO_INCREMENT",
                        "comment": "File ID.",
                    },
                    {
                        "name": "md5",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "File MD5.",
                    },
                    {
                        "name": "name",
                        "type_": "varchar(260)",
                        "constraint": "DEFAULT NULL",
                        "comment": "File name.",
                    },
                    {
                        "name": "size",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "File byte size.",
                    },
                    {
                        "name": "uploader",
                        "type_": "varchar(50)",
                        "constraint": "DEFAULT NULL",
                        "comment": "File uploader.",
                    }
                ],
                "primary": "id",
                "comment": "File information table."
            },

            ### "data".
            {
                "path": ("file", "data"),
                "fields": [
                    {
                        "name": "md5",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "File MD5.",
                    },
                    {
                        "name": "bytes",
                        "type_": "mediumblob",
                        "constraint": "NOT NULL",
                        "comment": "File bytes.",
                    }
                ],
                "primary": "md5",
                "comment": "File data table, storage files with size less than or equal to 16777215 bytes."
            },

            ### "data_big".
            {
                "path": ("file", "data_big"),
                "fields": [
                    {
                        "name": "md5",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "File MD5.",
                    },
                    {
                        "name": "bytes",
                        "type_": "longblob",
                        "constraint": "NOT NULL",
                        "comment": "File bytes.",
                    }
                ],
                "primary": "md5",
                "comment": "File data table, storage files with size greater than 16777215 bytes."
            }
        ]

        # Build.
        self.rdatabase.build(databases, tables)


    def upload(
        self,
        file: Union[str, bytes],
        name: Optional[str] = None,
        uploader: Optional[str] = None
    ) -> int:
        """
        Upload file to table `data` or `data_big` of database `file`.

        Parameters
        ----------
        file : File path or file bytes.
        name : File name.
            - `None` : Automatic set.
                * `parameter 'file' is 'str'` : Use path file name.
                * `parameter 'file' is 'bytes'` : Use file MD5.
            - `str` : Use this name.

        uploader : File uploader.

        Returns
        -------
        File ID.
        """

        # Get parameter.
        conn = self.rdatabase.connect()

        # Get parameter.

        ## File path.
        if file.__class__ == str:
            file_bytes = read_file(file)
            file_md5 = get_md5(file_bytes)
            file_name = os_basename(file)

        ## File bytes.
        elif file.__class__ == bytes:
            file_bytes = file
            file_md5 = get_md5(file_bytes)
            file_name = file_md5

        ## File name.
        if name is not None:
            file_name = name

        ## File size.
        file_size = len(file_bytes)

        ## Table name.
        if file_size > 16777215:
            table = "data_big"
        else:
            table = "data"

        # Exist.
        exist = conn.execute_exist(
            ("file", table),
            "`md5` = :file_md5",
            file_md5=file_md5
        )

        # Upload.

        ## Data.
        if not exist:
            data = {
                "md5": file_md5,
                "bytes": file_bytes
            }
            conn.execute_insert(
                ("file", table),
                data,
                "ignore"
            )

        ## Information.
        data = {
            "uploader": uploader,
            "md5": file_md5,
            "name": file_name,
            "size": file_size
        }
        conn.execute_insert(
            ("file", "information"),
            data,
            time=":NOW()"
        )

        # Get ID.
        file_id = conn.variables["identity"]

        # Commit.
        conn.commit()

        return file_id


    def download(
        self,
        id_: str,
        path: Optional[str] = None
    ) -> bytes:
        """
        Download file from table `data` or `data_big` of database `file`.

        Parameters
        ----------
        id_ : File ID.
        path : File save path.
            - `None` : Not save.
            - `str` : Save.
                * `File path` : Use this file path.
                * `Folder path` : Use this folder path and original name.

        Returns
        -------
        File bytes.
        """

        # Get information.

        ## Execute.
        result = self.rdatabase.execute_select(
            ("file", "information"),
            ["md5", "name", "size"],
            "`id` = :id_",
            limit=1,
            id_=id_
        )

        ## Check.
        if result.rowcount == 0:
            text = "file ID '%s' not exist" % id_
            raise ValueError(text)
        file_md5, file_name, file_size = result.first()

        # Download.

        ## Table name.
        if file_size > 16777215:
            table = "data_big"
        else:
            table = "data"

        ## Execute.
        result = self.rdatabase.execute_select(
            ("file", table),
            ["bytes"],
            "`md5` = :file_md5",
            limit=1,
            file_md5=file_md5
        )

        ## Check.
        if result.rowcount == 0:
            text = "file MD5 '%s' not exist" % file_md5
            raise ValueError(text)
        file_bytes = result.scalar()

        # Save.
        if path is not None:
            is_dir = os_isdir(path)
            if is_dir:
                path = os_join(path, file_name)
            write_file(path, file_bytes)

        return file_bytes