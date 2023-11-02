#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-04-24 09:20:04
LastEditors  : Kofi
LastEditTime : 2023-04-24 09:20:05
Description  : 绘图相关的命令
"""
from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from PyQt5.QtGui import QColor
from KofiPyQtHelper.models.PlotModel import DataPoint
from KofiPyQtHelper.components.MatplotlibFigure import MatplotlibFigure
from KofiPyQtHelper.components.CustomGraphics import CustomGraphics
from KofiPyQtHelper.utils.CommonHelper import CommonHelper
import pandas as pd
import numpy as np
from pathlib import Path


class GraphCommand:
    def __init__(self) -> None:
        self.commands.update(
            {
                "drawGraphics": self.drawGraphics,
                "loadFanOrCompIn": self.drawFanOrCompCharacteristicDiagram,
                "loadTurbineIn": self.drawTurbineCharacteristicDiagram,
                "loadCombustionChamber": self.drawCombustionChamberCharacteristicDiagram,
                "loadVariates": self.loadVariates,
            }
        )

    def drawGraphics(self, args):
        title = self.parameterSearchByName(args, "title")
        canvasName = self.parameterSearchByName(args, "canvasName")
        loadFun = self.parameterSearchByName(args, "loadFun")
        loadFile = self.parameterSearchByName(args, "fileName")

        if loadFile != None:
            currentFile = self.getCurrentInput(loadFile).text()
            if len(currentFile) > 0:
                if Path(currentFile).exists():
                    canvas = self.getCurrentInput(canvasName)
                    self.commands[loadFun](currentFile, title, canvas)
                else:
                    QMessageBox.about(self, "提示", "文件不存在")
            else:
                QMessageBox.about(self, "提示", "未选择文件")
        else:
            canvas = self.getCurrentInput(canvasName)
            self.commands[loadFun](args, canvas)

    def drawFanOrCompCharacteristicDiagram(
        self, file, title: str, canvas: MatplotlibFigure
    ):
        try:
            waccs, prcs, etacs, flag = self.getPropertyDiagramDatas(file, 4, True)
            if flag:
                datas = [
                    {
                        "layout": 211,
                        "x": "WACC",
                        "y": "PRC",
                        "datas": DataPoint(
                            "PRC", "red", x_array=waccs, y_array=prcs, isSegment=True
                        ),
                    },
                    {
                        "layout": 212,
                        "x": "WACC",
                        "y": "ETAC",
                        "datas": DataPoint(
                            "ETAC", "blue", x_array=waccs, y_array=etacs, isSegment=True
                        ),
                    },
                ]
                canvas.drawAxes(datas, title)
        except Exception as e:
            logger.exception(e)

    def splitArray(self, datas):
        datas = np.where(datas == "", np.nan, datas)
        datas = np.where(datas == "\t", "", datas)
        new_datas = [
            [
                float(item.strip())
                for item in row
                if not pd.isnull(item) and item.strip() != ""
            ]
            for row in datas
        ]
        # total = sum(len(sublist) for sublist in new_datas)
        return new_datas

    def drawTurbineCharacteristicDiagram(
        self, file, title: str, canvas: MatplotlibFigure
    ):
        try:
            pits, tffs, etats, flag = self.getPropertyDiagramDatas(file, 6, False)
            if flag:
                datas = [
                    {
                        "layout": 211,
                        "x": "PIT",
                        "y": "TFF",
                        "datas": DataPoint(
                            "TFF", "red", x_array=pits, y_array=tffs, isSegment=True
                        ),
                    },
                    {
                        "layout": 212,
                        "x": "PIT",
                        "y": "ETAT",
                        "datas": DataPoint(
                            "ETAT", "blue", x_array=pits, y_array=etats, isSegment=True
                        ),
                    },
                ]
                canvas.drawAxes(datas, title)
        except Exception as e:
            logger.exception(e)
            QMessageBox.about(self, "提示", "文件格式不正确")

    def drawCombustionChamberCharacteristicDiagram(
        self, file, title: str, canvas: MatplotlibFigure
    ):
        try:
            x_array, y_array, flag = self.verifyCombustionChamberData(file)
            if flag:
                datas = [
                    {
                        "layout": 111,
                        "x": "DELT",
                        "y": "ETAB",
                        "datas": DataPoint(
                            "DELT",
                            "red",
                            x_array=x_array,
                            y_array=y_array,
                            isSegment=True,
                        ),
                    },
                ]
                canvas.drawAxes(datas, title)

        except Exception as e:
            logger.exception(e)
            QMessageBox.about(self, "提示", "文件格式不正确")

    def verifyCombustionChamberData(self, file):
        flag = False
        x_array, y_array = [], []
        try:
            datas = pd.read_csv(
                file,
                header=None,
                delimiter="\n",
                error_bad_lines=False,
                skip_blank_lines=False,
                na_values=np.nan,
            )
            datas = (
                datas[0]
                .str.replace("\t", "")
                .str.split(",", expand=True)
                .replace("", np.nan)
            )

            array_lens = self.removal_null(datas.iloc[1])
            array_lens = [elem if not np.isnan(elem) else None for elem in array_lens]
            while None in array_lens:
                array_lens.remove(None)

            x_array = self.splitArray(datas.iloc[5:20].values)
            y_array = self.splitArray(datas.iloc[21:36].values)

            for array_index in range(len(array_lens)):
                if int(array_lens[array_index]) != len(x_array[array_index]) or int(
                    array_lens[array_index]
                ) != len(y_array[array_index]):
                    QMessageBox.about(self, "提示", "文件格式不正确")
                    raise RuntimeError("文件格式不正确")
            flag = True
        except Exception as e:
            flag = False
            logger.exception(e)
        finally:
            return x_array, y_array, flag

    def getPropertyDiagramDatas(self, file, index, flag, isChecked=True):
        """_summary_

        Args:
            file (_type_): 文件名称
            index (_type_): 开始读取的行数
            flag (_type_): 升序标识, True:升序, False:降序

        Raises:
            RuntimeError: _description_

        Returns:
            _type_: _description_
        """
        return_flag = False
        col1, col2, col3 = [], [], []
        try:
            if Path(file).exists():
                df = pd.read_csv(
                    file, header=None, sep=",", skiprows=1, skip_blank_lines=False
                )
                array_lens = self.removal_null(df.values[0])
                array_lens = [
                    elem if not np.isnan(elem) else None for elem in array_lens
                ]
                while None in array_lens:
                    array_lens.remove(None)

                col1 = self.split_array(df.iloc[index - 1 :, 0].values)
                col2 = self.split_array(df.iloc[index - 1 :, 1].values)
                col3 = self.split_array(df.iloc[index - 1 :, 2].values)

                if isChecked:
                    for array_index in range(len(array_lens)):
                        if (
                            int(array_lens[array_index]) != len(col1[array_index])
                            or int(array_lens[array_index]) != len(col2[array_index])
                            or int(array_lens[array_index]) != len(col3[array_index])
                        ):
                            QMessageBox.about(self, "提示", "文件格式不正确")
                            raise RuntimeError("文件格式不正确")

                    is_sorted = np.all(np.diff(col1[0]) >= 0)
                    if is_sorted == flag:
                        QMessageBox.about(self, "提示", "文件格式不正确")
                        raise RuntimeError("文件格式不正确")
                    else:
                        return_flag = True
        except Exception as e:
            logger.exception(e)
            QMessageBox.about(self, "提示", "文件格式不正确")
        finally:
            return col1, col2, col3, return_flag

    def formatLine(self, line):
        return line.replace("\t", "").replace("\n", "").replace("\r", "").strip()

    def loadVariates(self, args, canvas: MatplotlibFigure):
        filenames = []
        filenamesAppend = filenames.append
        variate = self.parameterSearchByName(args, "variates")
        for data in self.variates[variate]:
            if data["fileName"] not in filenames:
                filenamesAppend(data["fileName"])

        types = {}
        if len(filenames) > 0:
            for file in filenames:
                types[file] = pd.read_csv(
                    "./files/" + self.category + "/" + file + ".DAT",
                    sep=",",
                    encoding="utf8",
                    skip_blank_lines=False,
                )

        points = []

        featuresName = self.getCuttentInputValue("featuresName")
        features_y_coordinate = self.getCuttentInputValue("features_y_coordinate")

        if featuresName != "无":
            waccs, prcs, etacs, flag = self.getPropertyDiagramDatas(
                CommonHelper.getAbsFilePath(
                    "./files/{0}/{1}.dat".format(self.category, featuresName)
                ),
                1,
                False,
                False,
            )
            if features_y_coordinate == "RPC":
                points.append(
                    DataPoint("PRC", "red", x_array=waccs, y_array=prcs, isSegment=True)
                )
            elif features_y_coordinate == "ETAC":
                points.append(
                    DataPoint(
                        "ETAC", "red", x_array=waccs, y_array=etacs, isSegment=True
                    )
                )

        for item in self.variates[variate]:
            if type(types[item["fileName"]]) == list:
                x_array = []
                y_array = []
                for data in types[item["fileName"]]:
                    x_array.append(data[item["x"]])
                    y_array.append(data[item["y"]])
            else:
                x_array = self.split_array(
                    types[item["fileName"]].iloc[:, [item["x"]]].values
                )
                y_array = self.split_array(
                    types[item["fileName"]].iloc[:, [item["y"]]].values
                )

            color = QColor.colorNames()[item["color"]]

            points.append(
                DataPoint(
                    item["labelName"],
                    color,
                    x_array=x_array,
                    y_array=y_array,
                    isSegment=True,
                )
            )

        canvas.drawAxesMultipoint(
            points,
            self.variates["title"],
            self.variates["xlabel"],
            self.variates["ylabel"],
        )

    def split_array(self, items):
        arr = self.removal_null(items)

        nan_indices = np.isnan(arr)
        if not np.any(nan_indices):
            return arr.reshape(1, -1)
        split_points = np.where(nan_indices)[0]
        datas = [
            arr[sl:sr]
            for sl, sr in zip(
                np.concatenate([[0], split_points + 1]),
                np.concatenate([split_points, [len(arr)]]),
            )
        ]

        new_datas = [x for x in datas if len(x) > 0]

        return new_datas

    def removal_null(self, items):
        arr = []
        for item in items:
            if type(item) == str:
                arr.append(float(item.strip()) if item.strip() != "" else np.nan)
            else:
                arr.append(item)
        return arr
