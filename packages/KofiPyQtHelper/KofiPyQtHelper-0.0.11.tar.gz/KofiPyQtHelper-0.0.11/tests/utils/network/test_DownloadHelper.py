#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-04 18:22:58
LastEditors  : Kofi
LastEditTime : 2023-08-04 18:23:00
Description  : 
"""

from KofiPyQtHelper.utils.test.KofiTestCase import KofiTestCase, handleException
from KofiPyQtHelper.utils.DownloaderHelper import DownloaderHelper
from KofiPyQtHelper.models.DownloadTask import DownloadTask
from KofiPyQtHelper.enums.DownloadTaskStatus import DownloadTaskStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class DownloaderHelperTest(KofiTestCase):
    def setUp(self):
        relative_path = "./tests/data/database.db"
        absolute_path = os.path.abspath(relative_path)
        if os.path.exists(absolute_path):
            self.engine = create_engine("sqlite:///{}".format(absolute_path))
            self.Session = sessionmaker(bind=self.engine)
        self.downloadHelper = DownloaderHelper(self.Session())
        self.url = "https://dldir1.qq.com/weixin/mac/WeChatMac.dmg"
        self.save_path = "/Users/kofi/Downloads"

    def tearDown(self):
        # 在每个测试方法执行后关闭数据库连接
        self.Session.close_all()
        self.engine.dispose()

    @handleException
    def test_create_task_by_model(self):
        task = DownloadTask(
            url=self.url,
            save_path=self.save_path,
            status=DownloadTaskStatus.PAUSED.value,
        )
        task.init_value()
        session = self.Session()
        session.add(task)
        session.commit()

        saved_task = session.query(DownloadTask).filter_by(url=self.url).first()
        self.assertEqual(saved_task.url, self.url)

    @handleException
    def test_create_task(self):
        task = self.downloadHelper.create_download_task(self.url, self.save_path)
        saved_task = self.downloadHelper.get_download_task(task.id)
        self.assertEqual(saved_task.save_path, self.save_path)

    @handleException
    def test_start_task(self):
        task = self.downloadHelper.create_download_task(self.url, self.save_path)
        # thread_mock = mock.Mock()
        # self.downloadHelper.start_download_task = mock.Mock(return_value=thread_mock)
        self.downloadHelper.start_download_task(task.id)
        downloaded_task = self.downloadHelper.get_download_task(task.id)
        self.assertEqual(downloaded_task.status, DownloadTaskStatus.COMPLETED.value)
        self.assertEqual(downloaded_task.progress, float(1))
        # self.assertEqual(result, thread_mock)
        # self.downloadHelper.start_download_task.assert_called_once_with(task.id)

    @handleException
    def test_pause_task(self):
        task = self.downloadHelper.create_download_task(self.url, self.save_path)
        self.downloadHelper.start_download_task(task.id)
        current = self.downloadHelper.get_download_task(task.id)
        self.assertEqual(current.status, DownloadTaskStatus.DOWNLOADING.value)
        self.downloadHelper.pause_download_task(task.id)
        saved_task = self.downloadHelper.get_download_task(task.id)
        self.assertEqual(saved_task.status, DownloadTaskStatus.PAUSED.value)
