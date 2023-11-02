#!/usr/bin/env python
# coding=utf-8
"""
Author       : Kofi
Date         : 2022-07-27 10:47:31
LastEditors  : Kofi
LastEditTime : 2022-08-15 16:23:58
Description  : 通用函数
"""

import json, os, time
from loguru import logger
from functools import wraps


class CommonHelper:
    @staticmethod
    def readQss(style):
        try:
            with open(style, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return None

    @staticmethod
    def getItems(enums, type: str = "name"):
        items = []
        for k, v in enums.__members__.items():
            if type == "name":
                items.append(k)
            else:
                items.append(v.value)
        return items

    def load_data_from_json(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def Notepad(filename):
        os.system("start /B notepad " + CommonHelper.getFilePath(filename))

    @staticmethod
    def getFilePath(fileName):
        return os.path.join(os.getcwd(), fileName)

    @staticmethod
    def getAbsFilePath(fileName):
        try:
            return os.path.abspath(fileName)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def merageDict(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def runExe():
        pass

    def load_ui_file():
        pass

    def load_ui_configuration():
        pass

    def load_template(file):
        pass

    def load_data():
        pass

    def save_data():
        pass

    def generate_file():
        pass


def timeConsuming(func):
    """
    Decorator that reports the execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"耗时：{end-start}秒")
        return result

    return wrapper
