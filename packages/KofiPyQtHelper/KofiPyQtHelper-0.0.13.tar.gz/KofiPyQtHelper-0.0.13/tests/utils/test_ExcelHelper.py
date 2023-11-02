#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-31 11:16:27
LastEditors  : Kofi
LastEditTime : 2023-07-31 11:16:29
Description  : 
"""

from KofiPyQtHelper.utils.test.KofiTestCase import KofiTestCase, handleException

# import unittest
from KofiPyQtHelper.utils.ExcelHelper import ExcelHelper


class ExcelHelperTest(KofiTestCase):
    excel_file_name = "tests/data/test.xlsx"
    sheet_name = "选择方案"
    sheet_has_mutiple_header_name = "test"
    target_column_names = [
        {
            "sheet_name": "选择方案",
            "sheet_name_english": "xzfa",
            "columns": [
                "专业分类",
                "专业",
                "姓名",
                "准考证",
                "身份证",
                "手机号",
                "是否省内",
                "成绩排序",
                "文化课成绩",
                "语文成绩",
                "选择方案顺序",
            ],
            "column_names_english": [
                "zyfl",
                "zy",
                "xm",
                "zkz",
                "sfz",
                "sjh",
                "sfsn",
                "cjpx",
                "whkcj",
                "ywcj",
                "xzfasc",
            ],
        },
        {
            "sheet_name": "选择分配结果",
            "sheet_name_english": "xzfpjg",
            "columns": [
                "专业分类",
                "专业",
                "姓名",
                "准考证",
                "身份证",
                "手机号",
                "是否省内",
                "成绩排序",
                "选择方案顺序",
                "专业排名",
            ],
            "column_names_english": [
                "zymc",
                "zy",
                "xm",
                "zkz",
                "sfz",
                "sjh",
                "sfsn",
                "cjpx",
                "xzfasc",
                "zypm",
            ],
        },
        {
            "sheet_name": "未选择学生",
            "sheet_name_english": "wxzxs",
            "columns": [
                "手机号",
                "专业录取类别",
                "学生姓名",
                "准考证",
                "身份证",
                "是否省内",
                "成绩排序",
                "最后一次登录时间",
            ],
            "column_names_english": [
                "sjh",
                "zylqlb",
                "xsxm",
                "zkz",
                "sfz",
                "sfsn",
                "cjpx",
                "zhycdlsj",
            ],
        },
        {
            "sheet_name": "异常学生",
            "sheet_name_english": "ycxs",
            "columns": [
                "手机号",
                "专业录取类别",
                "学生姓名",
                "准考证",
                "身份证",
                "是否省内",
                "成绩排序",
                "最后一次登录时间",
            ],
            "column_names_english": [
                "sjh",
                "zylqlb",
                "xsxm",
                "zkz",
                "sfz",
                "sfsn",
                "cjpx",
                "zhycdlsj",
            ],
        },
    ]

    @handleException
    def test_get_sheet_names(self):
        sheet_names = ExcelHelper.getSheetNames(self.excel_file_name)
        target_sheet_names = [obj["sheet_name"] for obj in self.target_column_names]
        self.assertEqual(len(sheet_names), len(target_sheet_names))
        self.assertEqual(sheet_names, target_sheet_names)

    @handleException
    def test_get_column_names_by_sheet(self):
        column_names = ExcelHelper.getColumnNamesBySheet(
            self.excel_file_name, self.sheet_name
        )
        target_column_names = [
            obj for obj in self.target_column_names if obj["sheet_name"] == "选择方案"
        ][0]["columns"]
        print(target_column_names)
        print(column_names)
        self.assertEqual(len(column_names), len(target_column_names))
        self.assertEqual(column_names, target_column_names)

    @handleException
    def test_get_all_column_names_group_by_sheet(self):
        current_column_names = ExcelHelper.getAllColumnNamesGroupBySheet(
            self.excel_file_name
        )
        target_column_names = [
            {"sheet_name": obj["sheet_name"], "columns": obj["columns"]}
            for obj in self.target_column_names
        ]
        self.assertEqual(
            len(current_column_names),
            len(self.target_column_names),
        )
        self.assertEqual(current_column_names, target_column_names)

    @handleException
    def test_get_all_column_names_group_by_sheet_has_english_name(self):
        current_column_names = ExcelHelper.getAllColumnNamesGroupBySheet(
            self.excel_file_name
        )
        target_column_names = [
            {"sheet_name": obj["sheet_name"], "columns": obj["columns"]}
            for obj in self.target_column_names
        ]
        self.assertEqual(len(current_column_names), len(self.target_column_names))
        self.assertEqual(current_column_names, target_column_names)
