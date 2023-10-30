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

        # Build.
        self.build()


    def build(self) -> None:
        """
        `Check` and `build` all standard databases and tables.
        Include database `file` and table `information`, `data`.
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
                "path": "file.information",
                "fields": [
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "File upload time.",
                    },
                    {
                        "name": "uploader",
                        "type_": "varchar(50)",
                        "constraint": "DEFAULT NULL",
                        "comment": "File uploader.",
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
                        "type_": "mediumint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "File byte size.",
                    }
                ],
                "primary": "id",
                "comment": "File information."
            },

            ### "data".
            {
                "path": "file.data",
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
                "comment": "File data."
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
        `Upload` file.

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

        ## file name.
        if name is not None:
            file_name = name

        ## file size.
        file_size = len(file_bytes)

        # Exist.
        exist = self.rdatabase.execute_exist(
            ("file", "data"),
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
            self.rdatabase.execute_insert(
                ("file", "data"),
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
        self.rdatabase.execute_insert(
            ("file", "information"),
            data,
            time=":NOW()"
        )

        # Get ID.
        file_id = self.rdatabase.variables["identity"]

        return file_id


    def download(
        self,
        id_: str,
        path: Optional[str] = None
    ) -> bytes:
        """
        `Download` file.

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

        # Get parameter.
        if path is not None:
            is_dir = os_isdir(path)
        else:
            is_dir = False

        # Download.

        ## Generate SQL.
        if is_dir:
            sql_name = (
                "(\n"
                "    SELECT `name`\n"
                "    FROM `file`.`information`\n"
                "    WHERE `id` = :id_\n"
                "    LIMIT 1\n"
                ") AS `name`"
            )
        else:
            sql_name = "NULL AS `name`"
        sql = (
            f"SELECT `bytes`, {sql_name}\n"
            "FROM `file`.`data`\n"
            "WHERE EXISTS(\n"
            "    SELECT 1\n"
            "    FROM `file`.`information`\n"
            "    WHERE `id` = :id_\n"
            ")\n"
            "LIMIT 1"
        )

        ## Execute SQL.
        result = self.rdatabase(sql, id_=id_, report=True)

        # Check.
        if result.rowcount == 0:
            raise ValueError("file ID not exist")
        else:
            file_bytes, file_name = result.first()

        # Save.
        if path is not None:
            if is_dir:
                path = os_join(path, file_name)
            write_file(path, file_bytes)

        return file_bytes