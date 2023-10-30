# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-29 20:01:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database file methods.
"""


from .rdatabase import RDatabase


class RDBFile(object):
    """
    Rey's `database file` type.
    """


    def __init__(self, rengine: RDatabase) -> None:
        """
        Build `database file` instance.

        Parameters
        ----------
        rengine : RDatabase object.
        """

        # Set attribute.
        self.rengine = rengine