#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-08-17 19:39:37
LastEditors  : Kofi
LastEditTime : 2022-08-17 19:39:37
Description  : 
"""

from enum import Enum


class ColumnType(Enum):
    Text = "text"
    ChildrenText = "children_text"
    Flag = "flag"
    Enable = "enable"
    Enums = "enums"
    Hidden = "hidden"
    Buttons = "buttons"
