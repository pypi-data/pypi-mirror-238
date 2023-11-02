#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-04 06:55:25
LastEditors  : Kofi
LastEditTime : 2023-08-04 06:55:26
Description  : 
"""
from KofiPyQtHelper.repositories.BaseRepository import BaseRepository
from KofiPyQtHelper.models.DownloadTask import DownloadTask
from KofiPyQtHelper.enums.DownloadTaskStatus import DownloadTaskStatus


class DownloadTaskRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, DownloadTask)

    def updates(self, model):
        current = self.session.query(DownloadTask).filter_by(id=model.id).first()
        if current:
            self.session.merge(model)
            super().update()
        else:
            model.status = DownloadTaskStatus.PAUSED.value
            super().add(model)
