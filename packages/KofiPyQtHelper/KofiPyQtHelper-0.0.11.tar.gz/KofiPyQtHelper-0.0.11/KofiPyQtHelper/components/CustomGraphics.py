#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-04-18 16:40:34
LastEditors  : Kofi
LastEditTime : 2023-04-18 16:40:35
Description  : 
"""

from pyqtgraph import *
from loguru import logger
import numpy as np
import os, datetime
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QFont


class CustomGraphics(GraphicsLayoutWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont()
        self.font.setBold(False)
        self.setBackground("w")
        self.leftButtonPan = False
        # self.setMouseTracking(True)
        self.plots = []

    def drawAxes(self, items, title):
        self.clean()
        bx = None
        for item in items:
            point = item["datas"]
            if bx != None:
                plot_item = self.addPlot(row=1, col=0)
                plot_item.setXLink(bx)
            else:
                plot_item = self.addPlot(row=0, col=0)
                plot_item.setTitle(title, size="18pt", color="black")
            if point.isSegment:
                legend = LegendItem()
                legend.setBrush("w")
                legend.setPen("black")
                legend.setParentItem(plot_item)
                for i in range(len(point.x_array)):
                    data = plot_item.plot(
                        point.x_array[i],
                        point.y_array[i],
                        pen=point.color,
                        name=point.label,
                        symbolBrush=point.color,
                        symbolSize=4,
                    )
                    if i == 0:
                        legend.addItem(data, point.label)
                        legend.setParentItem(plot_item.graphicsItem())
                        legend.anchor((1, 0), (1, 0))
            else:
                plot_item.plot(
                    point.x_array,
                    point.y_array,
                    pen=point.color,
                    name=point.label,
                    symbolBrush=point.color,
                    symbolSize=4,
                )
            minx, miny = min(map(min, point.x_array)), min(map(min, point.y_array))
            maxx, maxy = max(map(max, point.x_array)), max(map(max, point.y_array))
            plot_item.getViewBox().setRange(xRange=[minx, maxx], yRange=[miny, maxy])
            plot_item.setLabel("left", text=item["y"], color="black")
            plot_item.setLabel("bottom", text=item["x"], color="black")
            bx = plot_item
            self.plots.append(
                {
                    "plot": plot_item,
                    "xRange": [minx, maxx],
                    "yRange": [miny, maxy],
                    "padding": min(minx * 0.1, miny * 0.1),
                }
            )
        self.setPlotMouseEnabled()

    def drawAxesMultipoint(self, items, title, xlabel, ylabel):
        self.clean()
        try:
            plot = self.addPlot()
            legend = LegendItem()
            legend.setParentItem(plot)
            legend.setBrush("w")
            legend.setPen("black")
            legend.anchor((1, 0), (1, 0))
            minx, miny = float("inf"), float("inf")
            maxx, maxy = float("-inf"), float("-inf")
            for point in items:
                if point.isSegment:
                    for i in range(len(point.x_array)):
                        data = plot.plot(
                            np.array(point.x_array[i]).flatten(),
                            np.array(point.y_array[i]).flatten(),
                            pen=point.color,
                            symbolBrush=point.color,
                            symbolSize=4,
                            label=point.label if i == 0 else None,
                        )
                else:
                    data = plot.plot(
                        np.array(point.x_array).flatten(),
                        np.array(point.y_array).flatten(),
                        pen=point.color,
                        label=point.label,
                    )

                legend.addItem(data, point.label)

                minx, miny = min(min(map(min, point.x_array)), minx), min(
                    min(map(min, point.y_array)), miny
                )
                maxx, maxy = max(max(map(max, point.x_array)), maxx), max(
                    maxy, max(map(max, point.y_array))
                )

            plot.autoRange()

            plot.getViewBox().setRange(
                xRange=[minx, maxx], yRange=[miny, maxy], padding=0
            )
            plot.setTitle(title)
            plot.setLabel("left", text=ylabel, color="black")
            plot.setLabel("bottom", text=xlabel, color="black")

            self.plots.append(
                {
                    "plot": plot,
                    "xRange": [minx, maxx],
                    "yRange": [miny, maxy],
                    "padding": 0,
                }
            )
            self.setPlotMouseEnabled()
        except Exception as e:
            logger.exception(e)

    def clean(self):
        try:
            self.plots = []
            self.clear()
            self.update()
        except Exception as e:
            logger.exception(e)

    def setPlotMouseEnabled(self):
        for item in self.plots:
            item["plot"].setMouseEnabled(x=self.leftButtonPan, y=self.leftButtonPan)

    def pan(self):
        self.leftButtonPan = not self.leftButtonPan
        self.setPlotMouseEnabled()

    def saveImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            f"{now_time}.png",
            "Image Files (*.png *.jpg *.bmp)",
            options=options,
        )
        if fileName:
            img = self.grab()
            img.save(fileName)
            if os.path.exists(fileName):
                QMessageBox.about(self, "提示", "保存成功")

    def resetView(self):
        for data in self.plots:
            data["plot"].getViewBox().setRange(
                xRange=data["xRange"], yRange=data["yRange"], padding=data["padding"]
            )
