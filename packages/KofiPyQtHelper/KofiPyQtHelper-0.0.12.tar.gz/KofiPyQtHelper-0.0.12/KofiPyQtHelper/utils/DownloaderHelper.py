#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-01 17:40:58
LastEditors  : Kofi
LastEditTime : 2023-08-01 17:40:59
Description  : 
"""
from KofiPyQtHelper.services.DownloadTaskService import DownloadTaskService


class DownloaderHelper:
    def __init__(self, session):
        self.task_service = DownloadTaskService(session)

    def create_download_task(self, url, file_path):
        return self.task_service.create_download_task(url, file_path)

    def start_download_task(self, task_id):
        self.task_service.start_download_task(task_id)

    def pause_download_task(self, task_id):
        self.task_service.pause_download_task(task_id)

    def delete_download_task(self, task_id):
        self.task_service.delete_download_task(task_id)

    def get_download_task(self, task_id):
        return self.task_service.get_download_task(task_id)

    def list_all_download_tasks(self):
        return self.task_service.list_all_download_tasks()

    def paginate_download_tasks(self, page, per_page):
        return self.task_service.paginate_download_tasks(page, per_page)
