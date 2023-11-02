#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-04-24 11:17:22
LastEditors  : Kofi
LastEditTime : 2023-04-24 11:17:23
Description  : 
"""
from loguru import logger
from PyQt5.QtWidgets import QMessageBox
from KofiPyQtHelper.utils.CommonHelper import CommonHelper
import copy


class WidgetCommand:
    def __init__(self) -> None:
        self.commands.update(
            {
                "editItemWindow": self.editItemWindow,
                "deleteItem": self.deleteItem,
                "close": self.close,
                "closeWindow": self.closeWindow,
                "openWindow": self.openWindow,
                "openWindowByCondition": self.openWindowByCondition,
                "openNotepad": self.openNotepad,
                "clearComponentValues": self.clearComponentValues,
                "listviewItemClicked": self.listviewItemClicked,
            }
        )

    def editItemWindow(self, args):
        fileName = self.parameterSearchByName(args, "fileName")
        title = self.parameterSearchByName(args, "title")
        width = self.parameterSearchByName(args, "width")
        height = self.parameterSearchByName(args, "height")
        variates = self.parameterSearchByName(args, "variates")
        currentData = copy.deepcopy(self.variates[variates])

        button = self.sender()
        if button:
            row = self.getCurrentInput(variates).indexAt(button.parent().pos()).row()

        self.initWindow(
            fileName,
            args,
            title,
            width,
            height,
            currentRow=row,
            loadData=False,
        )
        if hasattr(self, "currentType"):
            self.loadItems()
        self.initComponent(args)

        self.window.variates = currentData[row]
        self.window.initComponentValues()
        self.window.show()

    def deleteItem(self, args):
        variates = self.parameterSearchByName(args, "variates")
        # currentData = self.parameterSearchByName(args, "currentData")
        currentData = copy.deepcopy(self.variates[variates])
        buttonName = self.parameterSearchByName(args, "buttonName")
        length = self.parameterSearchByName(args, "listLength")
        button = self.sender()
        if button:
            row = self.getCurrentInput(variates).indexAt(button.parent().pos()).row()
            del currentData[row]
            self.variates[variates] = currentData
            self.setTableData(variates, self.variates[variates])

        if length != None:
            if len(self.variates[variates]) >= int(length):
                self.getCurrentInput(buttonName).setEnabled(False)
            else:
                self.getCurrentInput(buttonName).setEnabled(True)

    def closeWindow(self):
        self.parent.close()

    def openWindow(self, args):
        """打开窗口"""
        fileName = self.parameterSearchByName(args, "fileName")
        title = self.parameterSearchByName(args, "title")
        width = self.parameterSearchByName(args, "width")
        height = self.parameterSearchByName(args, "height")
        try:
            self.initWindow(fileName, args, title, width, height)
            self.initComponent(args)
            self.window.show()
        except Exception as e:
            logger.exception(e)
            QMessageBox.about(self, "提示", "设置打开失败")

    def openWindowByCondition(self, args):
        result = self.conditionalReturn(args)
        if result != None:
            fileName = result["fileName"]
            width = result["width"] if "width" in result else None
            height = result["height"] if "height" in result else None
            title = result["title"]
            if "currentType" in result:
                currentType = result["currentType"]
                components = result["components"]

        self.initWindow(fileName, args=args, title=title, width=width, height=height)
        if "currentType" in result:
            self.window.currentType = currentType
            self.window.componentNames = components
        if "openFileName" in result:
            currentResult = result["openFileName"]
            with open(
                "./files/{}/{}".format(self.category, currentResult["file"]),
                "r",
                encoding="utf-8",
            ) as f:
                obj = self.window.getCurrentInput(currentResult["componentName"])
                if obj != None:
                    obj.insertPlainText(f.read())
        self.window.show()

    def openNotepad(self, args):
        result = self.conditionalReturn(args)
        currenEngineType = self.getCuttentInputValue("engineType")
        for engine in self.engineTypeDatas:
            if engine["label"] == currenEngineType:
                engineType = engine["value"]
        if result != None:
            fileName = result["fileName"]
            CommonHelper.Notepad("./files/{}/{}".format(engineType, fileName))

    def listviewItemClicked(self, args):
        currentComponent = self.sender()
        index = currentComponent.currentIndex().row()
        component = self.getCurrentInput(currentComponent.attr)
        if component["command"][index] is not None:
            component["command"][index]()
        else:
            self.changeStack(currentComponent, component, index)

    def changeStack(self, currentComponent, componentInfo, index):
        self.getCurrentInput(componentInfo["stack"]).setCurrentIndex(
            componentInfo["items"][index]
        )
