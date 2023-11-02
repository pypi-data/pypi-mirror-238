#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-11-17 07:10:43
LastEditors  : Kofi
LastEditTime : 2022-11-17 07:10:43
Description  : 布局类
"""

from PyQt5.QtWidgets import (
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QStackedWidget,
)
from KofiPyQtHelper.components.FlowLayout import FlowLayout
from KofiPyQtHelper.utils.Ui.UiCommon import UiCommand


class LayoutHelper(UiCommand):
    def initTabwidget(self, parent: QWidget, info):
        tabWidget = QTabWidget()
        self.setPrivateProperty(info, tabWidget)
        tabWidget.setCurrentIndex(1)
        parent.addWidget(tabWidget)
        return tabWidget

    def setPrivateProperty(self, info, widget):
        if "name" in info:
            widget.setObjectName(info["name"])
        if "class" in info:
            widget.setProperty("class", info["class"])

    def initTab(self, parent: QTabWidget, info):
        tab = QWidget()
        self.setPrivateProperty(info, tab)
        layout = QVBoxLayout()
        self.setMargin(info, layout)
        tab.setLayout(layout)
        parent.addTab(tab, info["name"])
        return layout

    def initFrame(self, parent, info):
        frame = QFrame()
        self.setPrivateProperty(info, frame)
        if "shape" in info:
            frame.setFrameShape(QFrame.Shape[1])
            frame.setLineWidth(7)
        frame_layout = QVBoxLayout()
        self.setMargin(info, frame_layout)
        self.addToParentContainer(parent, frame, info)
        self.addToParentContainer(frame, frame_layout)
        return frame

    def initFormlayout(self, parent, info):
        form = QFormLayout()
        self.setPrivateProperty(info, form)

        self.addToParentContainer(parent, form, info)
        return form

    def initFlowlayout(self, parent, info):
        layout = FlowLayout()
        self.setPrivateProperty(info, layout)
        self.setMargin(info, layout)
        self.addToParentContainer(parent, layout, info)
        return layout

    def addToParentContainer(self, parent, current: QWidget, info):
        if "width" in info:
            current.setFixedWidth(info["width"])
        if "height" in info:
            current.setFixedHeight(info["height"])
        if isinstance(parent, QStackedWidget):
            parent.addWidget(current)
        elif hasattr(parent, "setLayout"):
            parent.setLayout(current)
        elif isinstance(parent, QLayout):
            if isinstance(parent, QGridLayout):
                parent.addWidget(
                    current,
                    self.gridInfo[parent]["currentRow"],
                    self.gridInfo[parent]["currentColumn"],
                )
                self.gridCalculate(parent)
            if isinstance(current, QLayout):
                parent.addLayout(current)
            else:
                parent.addWidget(current)
        else:
            parent.addWidget(current)

    def initHbox(self, parent: QWidget, info):
        widget = QWidget()
        self.setPrivateProperty(info, widget)
        hbox = QHBoxLayout()
        self.setMargin(info, hbox)
        if "spacing" in info:
            hbox.setSpacing(info["spacing"])
        widget.setLayout(hbox)

        self.addToParentContainer(parent, widget, info)
        return hbox

    def initVbox(self, parent, info):
        widget = QWidget()
        self.setPrivateProperty(info, widget)
        vbox = QVBoxLayout()
        self.setMargin(info, vbox)
        if "spacing" in info:
            vbox.setSpacing(info["spacing"])
        widget.setLayout(vbox)
        self.addToParentContainer(parent, widget, info)

        return vbox

    def initFrame(self, parent, info):
        frame = QFrame()
        self.setPrivateProperty(info, frame)
        self.addToParentContainer(parent, frame, info)

        return frame

    def initGridbox(self, parent, info):
        grid = QGridLayout()
        self.setPrivateProperty(info, grid)
        self.addToParentContainer(parent, grid, info)

        return grid

    def initGroupbox(self, parent, info):
        groupbox = QGroupBox(info["label"])
        self.setPrivateProperty(info, groupbox)

        layout_type = info.get("layout", "hbox").lower()
        layouts = {
            "hbox": QHBoxLayout,
            "vbox": QVBoxLayout,
            "gridbox": QGridLayout,
        }
        layout_cls = layouts.get(layout_type, QHBoxLayout)
        box = layout_cls()
        self.setMargin(info, box)
        groupbox.setLayout(box)
        if layout_type == "gridbox" and "columns" in info:
            self.initGridInfo(info, box)
        self.addToParentContainer(parent, groupbox, info)
        return box

    def initListwidget(self, parent: QWidget, info):
        widget = QListWidget()
        self.setPrivateProperty(info, widget)
        if "currentChanged" in info:
            commands = (
                self.commands[info["currentChanged"]]
                if isinstance(info["currentChanged"], str)
                else info["currentChanged"]
            )
            widget.currentChanged.connect(commands)
        else:
            widget.itemClicked.connect(self.listviewItemClicked)
        self.addToParentContainer(parent, widget, info)
        widget.attr = info["name"]
        self.components.append(
            {info["name"]: {"widget": widget, "stack": info["stack"]}}
        )
        return widget

    def initStack(self, parent, info):
        widget = QStackedWidget()
        self.setPrivateProperty(info, widget)
        self.addToParentContainer(parent, widget, info)
        if "name" in info:
            widget.attr = info["name"]
            self.components.append({info["name"]: widget})
        return widget

    def initStackitem(self, parent, info):
        return self.initVbox(parent, info)
