#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-04 09:57:56
LastEditors  : Kofi
LastEditTime : 2023-08-04 09:57:57
Description  : 
"""

from KofiPyQtHelper.models.DownloadTask import DownloadTask
from KofiPyQtHelper.services.BaseService import BaseService
from KofiPyQtHelper.repositories.DownloadTaskRepository import DownloadTaskRepository
from KofiPyQtHelper.enums.DownloadTaskStatus import DownloadTaskStatus
import time


class DownloadTaskService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.save_interval = 1
        self.taks_repository = DownloadTaskRepository(self.session)

    def create_download_task(self, url, file_path):
        download_task = DownloadTask(
            url=url, save_path=file_path, status=DownloadTaskStatus.PAUSED.value
        )
        download_task.init_value()
        self.taks_repository.add(download_task)
        return download_task

    def start_download_task(self, task_id):
        download_task = self.taks_repository.get(id=task_id)
        download_task.status = DownloadTaskStatus.DOWNLOADING.value
        self.taks_repository.update(download_task)
        threads = download_task.download_file()
        download_task.save_resume_file()
        while download_task.status == DownloadTaskStatus.DOWNLOADING.value:
            print(download_task.resume_file)
            progress = round(download_task.progress * 100)
            if progress >= 100:  # 使用大于等于判断下载是否完成
                if download_task.validate_file():
                    download_task.progress = 1.0
                    download_task.status = DownloadTaskStatus.COMPLETED.value
            self.taks_repository.update(download_task)
            time.sleep(self.save_interval)

        for thread in threads:
            thread.join()

        # download_task.status = DownloadTaskStatus.COMPLETED.value
        # self.taks_repository.update(download_task)

    def pause_download_task(self, task_id):
        download_task = self.taks_repository.get(id=task_id)
        if (
            download_task
            and download_task.status == DownloadTaskStatus.DOWNLOADING.value
        ):
            download_task.status = DownloadTaskStatus.PAUSED.value
            self.taks_repository.update(download_task)

    def delete_download_task(self, task_id):
        download_task = self.taks_repository.get(id=task_id)
        if download_task:
            self.taks_repository.delete(download_task)

    def get_download_task(self, task_id):
        return self.taks_repository.get(id=task_id)

    def list_all_download_tasks(self):
        return self.taks_repository.list_all()

    def resume_download(self, task_id):
        task = self.taks_repository.get(id=task_id)
        if task.status == DownloadTaskStatus.PAUSED.value:
            task.status = DownloadTaskStatus.DOWNLOADING.value
            self.taks_repository.update(task)
            task.resume_download()
            task.status = DownloadTaskStatus.COMPLETED.value
            self.taks_repository.update(task)
