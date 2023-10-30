# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database parameter methods.
"""


from typing import Dict, Union

from .rdatabase import RDatabase, RDBConnection


class RDBParameter(object):
    """
    Rey's `database parameters` type.
    """


    def __init__(
        self,
        rengine: Union[RDatabase, RDBConnection],
        global_: bool
    ) -> None:
        """
        Build `database parameters` instance.

        Parameters
        ----------
        rengine : RDatabase object or RDBConnection object.
        global_ : Whether base global.
        """

        # Set parameter.
        self.rengine = rengine
        self.global_ = global_


    def get(self) -> Dict[str, str]: ...


    def update(self, params: Dict[str, Union[str, float]]) -> None: ...


    def __getitem__(self, key: str) -> str:
        """
        Get item of parameter dictionary.

        Parameters
        ----------
        key : Parameter key.

        Returns
        -------
        Parameter value.
        """

        # Get.
        params = self.get()

        # Index.
        value = params[key]

        return value


    def __setitem__(self, key: str, value: Union[str, float]) -> None:
        """
        Set item of parameter dictionary.

        Parameters
        ----------
        key : Parameter key.
        value : Parameter value.
        """

        # Set.
        params = {key: value}

        # Update.
        self.update(params)


class RDBPStatus(RDBParameter):
    """
    Rey's `database parameter status` type.
    """


    def get(self) -> Dict[str, str]:
        """
        Get `parameter`.

        Returns
        -------
        Status of database.
        """

        # Generate SQL.

        ## Global.
        if self.global_:
            sql = "SHOW GLOBAL STATUS"

        ## Not global.
        else:
            sql = "SHOW STATUS"

        # Execute SQL.
        result = self.rengine(sql)

        # Convert dictionary.
        status = result.fetch_dict(val_field=1)

        return status


    def update(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `parameter`.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Throw exception.
        raise AssertionError("database status not update")


class RDBPVariable(RDBParameter):
    """
    Rey's `database parameter variable` type.
    """


    def get(self) -> Dict[str, str]:
        """
        Get `parameter`.

        Returns
        -------
        Variables of database.
        """

        # Generate SQL.

        ## Global.
        if self.global_:
            sql = "SHOW GLOBAL VARIABLES"

        ## Not global.
        else:
            sql = "SHOW VARIABLES"

        # Execute SQL.
        result = self.rengine(sql)

        # Convert dictionary.
        variables = result.fetch_dict(val_field=1)

        return variables


    def update(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `parameter`.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Generate SQL.
        sql_set_list = [
            "%s = %s" % (
                key,
                (
                    value
                    if value.__class__ in (int, float)
                    else "'%s'" % value
                )
            )
            for key, value in params.items()
        ]
        sql_set = ",\n    ".join(sql_set_list)

        # Global.
        if self.global_:
            sql = f"SET GLOBAL {sql_set}"

        ## Not global.
        else:
            sql = f"SET {sql_set}"

        # Execute SQL.
        self.rengine(sql)