#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-12-01 09:50:39
LastEditors  : Kofi
LastEditTime : 2022-12-01 09:50:39
Description  : Excel 工具类
"""
import openpyxl, os
import pandas as pd
from pypinyin import lazy_pinyin, Style
from loguru import logger


class ExcelHelper:
    @classmethod
    def loadExcelFile(cls, file_name: str, type: str = "pandas"):
        """_summary_
        加载Excel文件
        Args:
            file_name (str): _description_
        """
        try:
            if os.path.exists(file_name):
                if type == "pandas":
                    return pd.read_excel(file_name, sheet_name=None)
                elif type == "openpyxl":
                    return openpyxl.load_workbook(file_name)
            else:
                logger.info(f"文件{file_name}不存在")
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def readExcelToVariates(
        file_name: str, configs: list = None, sheet_name: str = None
    ):
        """_summary_
        读取Excel文件
        Args:
            config (str): _description_
            file_name (str): _description_
        """
        try:
            wb = openpyxl.load_workbook(file_name)
            sheet = wb[sheet_name] if sheet_name else wb.active

            for index, cell_value in enumerate(sheet[1]):
                for config in configs:
                    if config["title"] == cell_value.value:
                        config["index"] = index

            return sheet, configs

        except Exception as e:
            logger.exception(e)

    @staticmethod
    def getSheetNames(file_name: str):
        try:
            excelFile = ExcelHelper.loadExcelFile(file_name)
            return list(excelFile.keys())
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def getColumnNamesBySheet(file_name: str, sheet_name: str):
        try:
            excelFile = ExcelHelper.loadExcelFile(file_name)
            df = excelFile[sheet_name]
            return df.columns.tolist()
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def getAllColumnNamesGroupBySheet(file_name: str, has_english: bool = False):
        try:
            excelFile = ExcelHelper.loadExcelFile(file_name)
            if has_english:
                return [
                    {
                        "sheet_name": sheet,
                        "sheet_name_english": lazy_pinyin(
                            sheet, style=Style.FIRST_LETTER
                        ),
                        "columns": excelFile[sheet].columns.tolist(),
                        "column_names_english": [
                            lazy_pinyin(column, style=Style.FIRST_LETTER)
                            for column in excelFile[sheet].columns.tolist()
                        ],
                    }
                    for sheet in excelFile.sheet_names
                ]
            else:
                return [
                    {
                        "sheet_name": sheet,
                        "columns": excelFile[sheet].columns.tolist(),
                    }
                    for sheet in list(excelFile.keys())
                ]
        except Exception as e:
            logger.exception(e)


