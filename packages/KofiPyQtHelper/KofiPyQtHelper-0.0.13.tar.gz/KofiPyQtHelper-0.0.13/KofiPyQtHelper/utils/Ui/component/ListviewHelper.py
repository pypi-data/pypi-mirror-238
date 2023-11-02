#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:32:02
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:32:02
Description  : 
"""
from functools import partial
import os
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QListView,
    QListWidgetItem,
    QWidget,
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class ListviewHelper:
    def setHistorylistviewData(self):
        path = "./history/{}".format(self.category)
        try:
            engineTypes = [item.name for item in os.scandir(path)]
            slm = QStandardItemModel()
            for engineType in engineTypes:
                item = QStandardItem(engineType)
                slm.appendRow(item)
            return slm, engineTypes
        except OSError:
            # 处理目录不存在等异常情况
            return None, []

    def initHistroylistview(self, parent, info):
        listView = QListView()
        slm, engineTypes = self.setHistorylistviewData()
        listView.setModel(slm)

        listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.components.append({info["name"]: listView})
        self.items[info["name"]] = engineTypes
        parent.addWidget(listView)

    def initListwidgetitem(self, parent: QWidget, info):
        item = QListWidgetItem(info["label"])
        component = self.getCurrentInput(parent.attr)
        if "items" not in component:
            component["items"] = []
        if "command" not in component:
            component["command"] = []

        parent.addItem(item)
        if "command" in info:
            if type(info["command"]).__name__ == "str":
                if "params" in info:
                    commands = partial(self.commands[info["command"]], info["params"])
                else:
                    commands = self.commands[info["command"]]
            else:
                commands = info["command"]
            component["command"].append(commands)
            component["items"].append(None)
        else:
            item.attr = info["index"]
            component["command"].append(None)
            component["items"].append(info["index"])

        item.setSelected(info["selected"] if "selected" in info else False)
