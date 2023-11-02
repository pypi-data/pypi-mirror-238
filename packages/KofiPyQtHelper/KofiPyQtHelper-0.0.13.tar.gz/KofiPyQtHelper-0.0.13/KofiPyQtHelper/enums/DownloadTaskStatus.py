#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-04 10:46:35
LastEditors  : Kofi
LastEditTime : 2023-08-04 10:46:36
Description  : 
"""

from enum import Enum


class DownloadTaskStatus(Enum):
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
