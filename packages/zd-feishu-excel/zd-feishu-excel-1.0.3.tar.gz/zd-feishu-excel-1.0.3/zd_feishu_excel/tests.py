#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2023/10/27 2:37 PM
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------
import unittest
from .app import App
from .workbook import Workbook


class TestFeishuWorkbook(unittest.TestCase):
    def test_workbook(self):
        lzdApp = App(appid='', secret='')
        excel_ss_token = ''
        wb = Workbook(excel_ss_token, lzdApp)
        sheet = wb['Sheet1']
        print(sheet.cell(1, 1))
