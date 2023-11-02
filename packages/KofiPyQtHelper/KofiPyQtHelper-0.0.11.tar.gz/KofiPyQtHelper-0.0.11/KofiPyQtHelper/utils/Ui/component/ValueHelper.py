#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 16:09:53
LastEditors  : Kofi
LastEditTime : 2023-07-11 16:09:53
Description  : 
"""
from KofiPyQtHelper.enums import ComboboxValueType
from PyQt5.QtWidgets import QComboBox, QLineEdit, QTableWidget


class ValueHelper:
    def setComboValue(self, objInput: QComboBox, type: ComboboxValueType, items, val):
        if type == ComboboxValueType.index:
            val = val if val != "" else 0
            current_index = val
        elif type == ComboboxValueType.value:
            current_index = items.index(val)
        else:
            current_index = val

        objInput.setCurrentIndex(current_index)

    def setTextValue(self, objInput, val):
        objInput.setText(val)

    def getCurrentInput(self, name):
        for component in self.components:
            for key, objInput in component.items():
                if key == name:
                    return objInput
        return None

    def initComponentValues(self):
        for component in self.components:
            for key, objInput in component.items():
                if type(objInput) == QLineEdit:
                    self.setTextValue(objInput, str(self.variates[key]))
                elif type(objInput) == QComboBox:
                    # if key != "color":
                    self.setComboValue(
                        objInput,
                        self.items[key]["type"],
                        self.items[key]["data"],
                        self.variates[key],
                    )
                elif type(objInput) == QTableWidget:
                    self.setTableData(key, self.variates[key])

    def clearComponentValues(self):
        """清除组件的值,恢复为默认值"""
        for component in self.components:
            for key, objInput in component.items():
                if type(objInput) == QLineEdit:
                    self.variates[key] = ""
                    self.setTextValue(objInput, str(self.variates[key]))
                elif type(objInput) == QComboBox:
                    self.setComboValue(
                        objInput,
                        self.items[key]["type"],
                        self.items[key]["data"],
                        self.variates[key],
                    )
                elif type(objInput) == QTableWidget:
                    self.variates[key] = []
                    self.setTableData(key, self.variates[key])

    def getCuttentInputValue(self, name: str):
        """通过组件名称获取组件值
        Args:
            name (str): 组件名称

        Returns:
            str: 组件当前值
        """
        obj = self.getCurrentInput(name)
        if obj != None:
            current = (
                obj.text()
                if type(obj) == QLineEdit
                else obj.currentText()
                if type(obj) == QComboBox
                else None
            )
            return current
        return None
