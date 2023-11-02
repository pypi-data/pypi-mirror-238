#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/chatopera/store/sdk/python/demo.py
# Author: Hai Liang Wang
# Date: 2023-10-27:09:27:26
#
# ===============================================================================


class LicensedfileDownloadException(BaseException):
    '''
    File Download exception
    '''
    errcode = None
    errmsg = None

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return "LicensedfileDownloadException[%s] %s" % (self.errcode, self.errmsg)
