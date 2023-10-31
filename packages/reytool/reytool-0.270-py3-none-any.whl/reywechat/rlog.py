# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-19 11:33:45
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from os import mkdir as os_mkdir
from os.path import (
    abspath as os_abspath,
    exists as os_exists
)
from reytool.rlog import RLog


# __all__ = (
#     "RLog",
#     "rlog"
# )


# # Instance.
# name = "WeChatLog"
# rlog = RLog(name)

# # Add handler.

# ## File.
# log_folder_path = r".\log"
# log_file_path = r".\log\%s" % name
# if not os_exists(log_folder_path):
#     os_mkdir(log_folder_path)
# log_file_path = os_abspath(log_file_path)
# rlog.add_file(log_file_path, time="m")

# ## Print.
# rlog.add_print()