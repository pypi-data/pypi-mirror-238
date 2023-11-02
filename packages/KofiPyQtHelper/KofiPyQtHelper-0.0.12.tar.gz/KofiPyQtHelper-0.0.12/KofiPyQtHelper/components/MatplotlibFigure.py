#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-11-21 14:52:23
LastEditors  : Kofi
LastEditTime : 2022-11-21 14:52:23
Description  : 
"""
import matplotlib.pyplot as plt
import tkinter as tk
from loguru import logger
from matplotlib import font_manager
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from KofiPyQtHelper.utils.CommonHelper import CommonHelper
import matplotlib


class MatplotlibFigure(FigureCanvasQTAgg):
    def __init__(self, width=10, heigh=10, dpi=100):
        matplotlib.use("Qt5Agg")
        self.currentFont = font_manager.FontProperties(
            fname=CommonHelper.getAbsFilePath("./styles/fonts/SimHei.ttf")
        )
        plt.rcParams["axes.unicode_minus"] = False
        # plt.rcParams["toolbar"] = "toolmanager"
        plt.rcParams.update({"font.size": 10})

        plt.style.use(CommonHelper.getAbsFilePath("./styles/matlib.mplstye"))
        width = 10 if width == None else width
        heigh = 10 if heigh == None else heigh
        dpi = 70 if dpi == None else dpi

        self.fig = Figure(figsize=(width, heigh), dpi=dpi)
        self.plt = plt

        matplotlib.interactive(False)

        super(MatplotlibFigure, self).__init__(self.fig)  # 在父类种激活self.fig， 否则不能显示图像
        self.toolbar = NavigationToolbar(self.fig.canvas, self)
        self.toolbar.hide()

    def drawAxes(self, items, title):
        plt.clf()
        self.clear()  # 清除绘图区
        bx = None
        for item in items:
            if bx != None:
                ax = self.fig.add_subplot(item["layout"], sharex=bx)
            else:
                ax = self.fig.add_subplot(item["layout"])
            point = item["datas"]
            if point.isSegment:
                minx, miny = min(map(min, point.x_array)), min(map(min, point.y_array))
                maxx, maxy = max(map(max, point.x_array)), max(map(max, point.y_array))
                for i in range(len(point.x_array)):
                    ax.plot(
                        point.x_array[i],
                        point.y_array[i],
                        color=point.color,
                        marker=point.marker,
                        linewidth=0.5,
                        label=point.label if i == 0 else None,
                    )
                ax.set_xlim(minx, maxx)
                ax.set_ylim(miny, maxy)
            else:
                ax.plot(
                    point.x_array,
                    point.y_array,
                    color=point.color,
                    marker=point.marker,
                    linewidth=0.5,
                    label=point.label,
                )
            ax.set_xlabel(item["x"], fontproperties=self.currentFont)
            ax.set_ylabel(item["y"], fontproperties=self.currentFont)
            ax.legend(prop=self.currentFont)
            bx = ax
        self.fig.suptitle(title, fontproperties=self.currentFont)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def drawAxesMultipoint(self, items, title, xlabel, ylabel):
        try:
            self.clear()
            axes = self.fig.add_subplot()

            for point in items:
                if point.isSegment:
                    for i in range(len(point.x_array)):
                        axes.plot(
                            point.x_array[i],
                            point.y_array[i],
                            color=point.color,
                            marker=point.marker,
                            linewidth=0.5,
                            label=point.label if i == 0 else None,
                        )
                else:
                    axes.plot(
                        point.x_array,
                        point.y_array,
                        color=point.color,
                        marker=point.marker,
                        linewidth=0.5,
                        label=point.label,
                    )

            current_minx, current_miny = min(map(min, point.x_array)), min(
                map(min, point.y_array)
            )
            current_maxx, current_maxy = max(map(max, point.x_array)), max(
                map(max, point.y_array)
            )

            axes.set_xlim(current_minx, current_maxx)
            axes.set_ylim(current_miny, current_maxy)
            axes.set_xlabel(xlabel, fontproperties=self.currentFont)
            axes.set_ylabel(ylabel, fontproperties=self.currentFont)
            axes.legend(prop=self.currentFont)

            self.fig.suptitle(title, fontproperties=self.currentFont)
            self.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
            self.fig.canvas.flush_events()  # 画布刷
        except Exception as e:
            logger.exception(e)

    def clear(self):
        self.fig.clear()

    def home(self):
        self.toolbar.home()

    def zoom(self):
        self.toolbar.zoom()

    def pan(self):
        self.toolbar.pan()

    def save(self):
        self.toolbar.save_figure()
