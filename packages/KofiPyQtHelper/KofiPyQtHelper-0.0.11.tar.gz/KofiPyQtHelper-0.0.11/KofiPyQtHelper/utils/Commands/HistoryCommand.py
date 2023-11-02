#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-04-24 08:31:46
LastEditors  : Kofi
LastEditTime : 2023-04-24 08:31:47
Description  : 历史数据相关的命令
"""
from KofiPyQtHelper.utils.CommonHelper import CommonHelper
import shutil, os
from loguru import logger
from PyQt5.QtWidgets import QMessageBox


class HistoryCommand:
    def __init__(self) -> None:
        self.commands.update(
            {
                "loadHistory": self.loadHistory,
                "deleteHistory": self.deleteHistory,
                "saveHistory": self.saveHistory,
            }
        )

    def deleteHistory(self, args):
        listView, engineType, currentName, path = self.getHistoryListData()
        if currentName != None:
            reply = QMessageBox.question(
                self,
                "确认",
                "是否删除<font color='blue' size='+1'>{}</font>中的,<font color='red'>{}</font>方案".format(
                    engineType, currentName
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if reply == QMessageBox.Yes:
                shutil.rmtree(path)
                slm, _ = self.setHistorylistviewData()
                listView.setModel(slm)
                self.items["history"].remove(currentName)
                currentName = None
                QMessageBox.about(self, "提示", "删除成功")
        else:
            QMessageBox.about(self, "提示", "未选择历史方案")

    def getHistoryListData(self):
        listView = self.getCurrentInput("history")
        item = listView.currentIndex().row()

        if item != -1:
            currentName = self.items["history"][item]
            path = CommonHelper.getAbsFilePath(
                "./history/{}/{}".format(self.category, currentName)
            )
        else:
            currentName = None
            path = None

        engineTypeDict = {
            engine["value"]: engine["label"] for engine in self.engineTypeDatas
        }
        engineType = engineTypeDict.get(self.category, None)

        return listView, engineType, currentName, path

    def saveHistory(self, args):
        path = CommonHelper.getAbsFilePath(
            "./history/{}/{}".format(self.category, self.variates["fileName"])
        )
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.join(path, "datas"), exist_ok=True)
                os.makedirs(os.path.join(path, "files"), exist_ok=True)

                datasPath = CommonHelper.getAbsFilePath(
                    "./config/datas/{}".format(self.category)
                )
                filesPath = CommonHelper.getAbsFilePath(
                    "./files/{}".format(self.category)
                )

                for file in os.listdir(datasPath):
                    shutil.copy(
                        os.path.join(datasPath, file), os.path.join(path, "datas", file)
                    )

                for file in os.listdir(filesPath):
                    _, ext = os.path.splitext(file)
                    if ext.lower() != ".exe":
                        shutil.copy(
                            os.path.join(filesPath, file),
                            os.path.join(path, "files", file),
                        )

                QMessageBox.about(self, "提示", "保存成功")
                self.close()
            except Exception as e:
                logger.exception(e)
                shutil.rmtree(path)
                QMessageBox.about(self, "提示", "保存失败")
        else:
            QMessageBox.about(self, "提示", "保存失败,方案名称重复.请更换方案名称.")

    def loadHistory(self, args):
        _, engine_type, current_name, path = self.getHistoryListData()

        if current_name is None:
            QMessageBox.about(self, "提示", "未选择历史方案")
            return

        reply = QMessageBox.question(
            self,
            "确认",
            f"是否加载<font color='blue' size='+1'>{engine_type}</font>中的,<font color='red'>{current_name}</font>方案",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply != QMessageBox.Yes:
            return

        datas_path = CommonHelper.getAbsFilePath(f"./config/datas/{self.category}")
        files_path = CommonHelper.getAbsFilePath(f"./files/{self.category}")

        for sub_dir in ["datas", "files"]:
            src_dir = os.path.join(path, sub_dir)
            dst_dir = datas_path if sub_dir == "datas" else files_path
            for file_name in os.listdir(src_dir):
                src_file = os.path.join(src_dir, file_name)
                dst_file = os.path.join(dst_dir, file_name)
                shutil.copy(src_file, dst_file)

        QMessageBox.about(self, "提示", "加载成功")
        self.close()
