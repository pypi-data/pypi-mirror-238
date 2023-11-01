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
        Check and build all standard databases and tables.
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
                        "name": "id",
                        "type_": "mediumint unsigned",
                        "constraint": "NOT NULL AUTO_INCREMENT",
                        "comment": "File ID.",
                    },
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "File upload time.",
                    },
                    {
                        "name": "md5",
                        "type_": "char(32)",
                        "constraint": "NOT NULL",
                        "comment": "File MD5.",
                    },
                    {
                        "name": "size",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "File byte size.",
                    },
                    {
                        "name": "name",
                        "type_": "varchar(260)",
                        "constraint": "DEFAULT NULL",
                        "comment": "File name.",
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
                        "type_": "char(32)",
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
                "comment": "File data table."
            }
        ]

        ## View stats.
        views_stats = [

            ### "stats".
            {
                "path": ("file", "stats"),
                "items": [
                    {
                        "name": "count",
                        "select": (
                            "SELECT COUNT(1)\n"
                            "FROM `file`.`information`"
                        ),
                        "comment": "File information count."
                    },
                    {
                        "name": "count_data",
                        "select": (
                            "SELECT COUNT(1)\n"
                            "FROM `file`.`data`"
                        ),
                        "comment": "File data unique count."
                    },
                    {
                        "name": "count_uploader",
                        "select": (
                            "SELECT COUNT(1)\n"
                            "FROM (\n"
                            "    SELECT 1\n"
                            "    FROM `file`.`information`\n"
                            "    WHERE `uploader` IS NOT NULL\n"
                            "    GROUP BY `uploader`\n"
                            ") AS `uploader_group`"
                        ),
                        "comment": "File uploader unique count."
                    },
                    {
                        "name": "size_avg",
                        "select": (
                            "SELECT CONCAT(\n"
                            "    ROUND(AVG(`size`) / 1024),\n"
                            "    ' KB'\n"
                            ")\n"
                            "FROM `file`.`information`\n"
                        ),
                        "comment": "File average size."
                    },
                    {
                        "name": "size_max",
                        "select": (
                            "SELECT CONCAT(\n"
                            "    ROUND(MAX(`size`) / 1024),\n"
                            "    ' KB'\n"
                            ")\n"
                            "FROM `file`.`information`\n"
                        ),
                        "comment": "File maximum size."
                    },
                    {
                        "name": "last_time",
                        "select": (
                            "SELECT MAX(`time`)\n"
                            "FROM `file`.`information`"
                        ),
                        "comment": "File last upload time."
                    },
                ]
            }
        ]

        # Build.
        self.rdatabase.build(databases, tables, views_stats=views_stats)


    def upload(
        self,
        file: Union[str, bytes],
        name: Optional[str] = None,
        uploader: Optional[str] = None
    ) -> int:
        """
        Upload file.

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

        # Exist.
        exist = conn.execute_exist(
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
            conn.execute_insert(
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
        Download file.

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

        # Generate SQL.
        sql = (
            "SELECT `name`, (\n"
            "    SELECT `bytes`\n"
            "    FROM `file`.`data`\n"
            "    WHERE `md5` = `information`.`md5`\n"
            "    LIMIT 1\n"
            ") AS `bytes`\n"
            "FROM `file`.`information`\n"
            "WHERE `id` = :id_\n"
            "LIMIT 1"
        )

        # Execute SQL.
        result = self.rdatabase(sql, id_=id_)

        # Check.
        if result.empty:
            text = "file ID '%s' not exist or no data" % id_
            raise ValueError(text)
        file_name, file_bytes = result.first()

        # Save.
        if path is not None:
            is_dir = os_isdir(path)
            if is_dir:
                path = os_join(path, file_name)
            write_file(path, file_bytes)

        return file_bytes


    __call__ = build