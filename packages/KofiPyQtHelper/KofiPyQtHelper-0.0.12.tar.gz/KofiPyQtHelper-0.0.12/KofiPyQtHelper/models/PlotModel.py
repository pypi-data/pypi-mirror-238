#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-08-29 08:10:54
LastEditors  : Kofi
LastEditTime : 2022-08-29 08:10:55
Description  : 图形模型
"""


from array import array
from dataclasses import dataclass, field
from typing import List
import numpy as np


@dataclass
class DataPoint:
    label: str
    color: str
    x_array: array
    y_array: array
    isSegment: bool = False
    marker: str = "."

    @property
    def XMin(self):
        x = np.array(self.x_array)
        if x.ndim == 1:
            return min(self.x_array)
        elif x.ndim == 2:
            return min(map(min, self.x_array))

    @property
    def XMax(self):
        return max(self.x_array)

    @property
    def YMin(self):
        return min(self.y_array)

    @property
    def YMax(self):
        return max(self.y_array)


@dataclass
class plotModel:
    x_label: str
    y_label: str
    title: str
    data_points: List[DataPoint] = field(default_factory=list)

    @property
    def XYScope(self):
        xMins, xMaxs, yMins, yMaxs = [], [], [], []
        xMinsAppent = xMins.append
        xMaxsAppent = xMaxs.append
        yMinsAppent = yMins.append
        yMaxsAppent = yMaxs.append
        for dataPoint in self.data_points:
            xMinsAppent(dataPoint.XMin)
            xMaxsAppent(dataPoint.XMax)

            yMinsAppent(dataPoint.YMin)
            yMaxsAppent(dataPoint.YMax)

        return {
            "x": {"min": min(xMins), "max": max(xMaxs)},
            "y": {"min": min(yMins), "max": max(yMaxs)},
        }

    def add_data_point(self, dataPoint: DataPoint):
        self.data_points.append(dataPoint)
