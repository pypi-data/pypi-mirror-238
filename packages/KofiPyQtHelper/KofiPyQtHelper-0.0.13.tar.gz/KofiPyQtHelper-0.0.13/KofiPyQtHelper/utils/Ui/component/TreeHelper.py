#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:32:02
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:32:02
Description  : 
"""

from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem


class TreeHelper:
    def initTree(self, parent: QWidget, info):
        tree = QTreeWidget()
        self.initTreeHeader(tree, info)
        self.components.append({info["name"]: tree})
        self.trees[info["name"]] = info["columns"]
        self.setTreeData(tree, info, self.layout_datas)
        parent.addWidget(tree)

    def initTreeHeader(self, controls, info):
        controls.setColumnCount(len(info["columns"]))
        controls.setHeaderLabels(info["columns"])

    def setTreeData(self, parent, info, datas):
        for data in datas:
            item = QTreeWidgetItem(parent)
            i = 0
            for column in info["names"]:
                value = data[column] if column in data else ""
                item.setText(i, value.lower())
                i += 1
            if "content" in data:
                self.setTreeData(item, info, data["content"])
