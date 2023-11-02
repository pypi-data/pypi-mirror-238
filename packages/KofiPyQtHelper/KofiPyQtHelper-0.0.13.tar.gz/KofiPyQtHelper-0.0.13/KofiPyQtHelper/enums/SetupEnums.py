"""
Author       : Kofi
Date         : 2022-07-27 19:09:23
LastEditors  : Kofi
LastEditTime : 2022-08-12 10:46:33
Description  : 组件类型
"""

from enum import Enum


class SetupEnums(Enum):
    Tab = "tab"
    HBox = "hbox"
    VBox = "vbox"
    FormLayout = "formlayout"
    GroupBox = "groupbox"

    Frame = "frame"

    Stretch = "stretch"

    Button = "button"
    Table = "table"
    Textbox = "textbox"
    Hidden = "hidden"
    Combobox = "combobox"
    ColorCombo = "colorCombobox"
