#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:22:09
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:22:09
Description  : 
"""

from PyQt5.QtWidgets import QLayout
from loguru import logger


class UiCommand:
    def setMargin(self, info, box: QLayout):
        if "margins" in info:
            length = len(info["margins"])
            if length == 4:
                box.setContentsMargins(
                    info["margins"][1],
                    info["margins"][2],
                    info["margins"][3],
                    info["margins"][0],
                )
            elif length == 3:
                box.setContentsMargins(
                    info["margins"][1],
                    info["margins"][0],
                    info["margins"][1],
                    info["margins"][2],
                )
            elif length == 2:
                box.setContentsMargins(
                    info["margins"][1],
                    info["margins"][0],
                    info["margins"][0],
                    info["margins"][1],
                )
            elif length == 1:
                box.setContentsMargins(
                    info["margins"][0],
                    info["margins"][0],
                    info["margins"][0],
                    info["margins"][0],
                )
            else:
                box.setContentsMargins(info["margins"][0])
                logger.exception("{}-设置边框出现问题".format(info))
        else:
            box.setContentsMargins(5, 5, 5, 5)
