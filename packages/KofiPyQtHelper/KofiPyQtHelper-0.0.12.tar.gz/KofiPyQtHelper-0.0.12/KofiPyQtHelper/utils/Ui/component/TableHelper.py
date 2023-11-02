#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:27:34
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:27:34
Description  : 
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QTableWidgetItem
from KofiPyQtHelper.enums.ColumnType import ColumnType
from KofiPyQtHelper.components.Pagination import Pagination


class TableHelper:
    def initTable(self, parent: QWidget, info):
        table = QTableWidget()
        table.setObjectName(info["name"])
        if "height" in info:
            table.setFixedHeight(info["height"])
        self.initTableHeader(table, info["columns"])
        self.tables[info["name"]] = info["columns"]
        self.components.append({info["name"]: table})
        self.setTableData(info["name"], [])
        parent.addWidget(table)

    def initTableHeader(self, controls, info):
        columns = info["names"]
        controls.setColumnCount(len(info["header"]))
        controls.setHorizontalHeaderLabels(info["header"])
        controls.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        for index, column in enumerate(columns):
            if "width" in column:
                controls.setColumnWidth(index, column["width"])
            if column["type"] == "hidden":
                controls.setColumnHidden(index, True)

    def setTableData(self, name, datas):
        table = self.tables[name]
        columns = table["names"]
        current = self.getCurrentInput(name)
        self.initTableHeader(current, table)

        current.clearContents()
        self.variates[name] = list(datas)
        current.setEditTriggers(QAbstractItemView.NoEditTriggers)
        current.setRowCount(len(datas))

        def setItem(row, column, value, is_widget=False):
            if is_widget:
                current.setCellWidget(row, column, value)
            else:
                current.setItem(row, column, QTableWidgetItem(str(value)))

        value_setters = {
            ColumnType.Hidden: lambda value: None,
            ColumnType.Text: lambda value: value[key],
            ColumnType.Enums: lambda value: str(value[key].value)
            if row["item"] == "value"
            else str(value[key]),
            ColumnType.Flag: lambda value: item.get("data", ["否", "是"])[value[key]],
            ColumnType.Enable: lambda value: item.get("data", ["禁用", "启用"])[value[key]],
            ColumnType.ChildrenText: lambda value: str(
                value[key][item.get("index", 0)][item["value"]]
            ),
            ColumnType.Buttons: lambda value: self.createButtonLayout(
                item["content"], name
            ),
        }

        for row, data in enumerate(datas):
            for column, item in enumerate(columns):
                types = ColumnType(item.get("type", ColumnType.Text))
                key = item["name"]

                value_setter = value_setters.get(types, lambda value: value[key])
                value = value_setter(data)

                if types == ColumnType.Buttons:
                    setItem(row, column, value, is_widget=True)
                elif value is not None:
                    setItem(row, column, value)

        current.resizeColumnsToContents()

    def initPagination(self, parent: QWidget, info):
        pagination = Pagination(**info)
        self.components.append({info["name"]: pagination})
        parent.addWidget(pagination)
