#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-02 17:02:10
LastEditors  : Kofi
LastEditTime : 2023-08-02 17:02:12
Description  : 
"""
from KofiPyQtHelper.models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
import hashlib, os, threading, urllib, requests
from KofiPyQtHelper.enums.DownloadTaskStatus import DownloadTaskStatus
from loguru import logger


class DownloadTask(BaseModel):
    __tablename__ = "download_task"

    url = Column(String)
    chunk_size = Column(Integer, default=4096)
    num_threads = Column(Integer, default=4)
    save_path = Column(String)
    file_name = Column(String, default="")
    file_type = Column(String, default="")
    total_size = Column(Integer, default=0)
    downloaded_size = Column(Integer, default=0)
    progress = Column(Float, default=0.0)
    status = Column(String)
    resume_file = Column(String, default="")

    @hybrid_method
    def init_value(self):
        # response = urllib.request.urlopen(self.url)
        response = requests.head(self.url).headers
        if response:
            self.total_size = int(response.headers["Content-Length"])
            filename = urllib.parse.urlparse(self.url).path.split("/")[-1]
            self.file_type = os.path.splitext(filename)[1]
            self.file_name = filename

    @hybrid_property
    def lock(self):
        if not hasattr(self, "_lock"):
            self._lock = threading.Lock()
        return self._lock

    def calculate_chunk_hash(self, start_pos, end_pos):
        headers = {"Range": f"bytes={start_pos}-{end_pos}"}
        response = requests.get(self.url, headers=headers, stream=True)
        hasher = hashlib.sha256()

        for chunk in response.iter_content(chunk_size=self.chunk_size):
            if chunk:
                hasher.update(chunk)

        return hasher.hexdigest()

    def download_chunk(self, start_pos, end_pos):
        headers = {"Range": f"bytes={start_pos}-{end_pos}"}
        response = requests.get(self.url, headers=headers, stream=True, timeout=10)
        file_path = os.path.join(self.save_path, self.file_name)
        if not os.path.exists(file_path):
            mode = "wb+"
        else:
            mode = "rb+"

        with open(file_path, mode) as file:
            file.seek(start_pos)
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    if self.status != DownloadTaskStatus.DOWNLOADING.value:
                        return
                    try:
                        with self.lock:  # 使用互斥锁进行线程同步
                            self.downloaded_size += len(chunk)
                            self.progress = self.downloaded_size / self.total_size
                            file.write(chunk)
                    except Exception as e:
                        logger.error(e)

    def download_file(self, start_pos=0):
        chunk_size = self.total_size // self.num_threads
        threads = []
        for i in range(self.num_threads):
            range_start_pos = start_pos + i * chunk_size
            range_end_pos = (
                start_pos + (i + 1) * chunk_size - 1
                if i < self.num_threads - 1
                else self.total_size - 1
            )

            thread = threading.Thread(
                target=self.download_chunk, args=(range_start_pos, range_end_pos)
            )
            thread.start()
            threads.append(thread)

        # for thread in threads:
        #     thread.join()
        return threads

    def calculate_file_hash(self):
        hasher = hashlib.sha256()
        file_path = os.path.join(self.save_path, self.file_name)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    def validate_file(self):
        file_path = os.path.join(self.save_path, self.file_name)
        if os.path.exists(file_path):
            except_hash = self.calculate_file_hash()
            return except_hash == self.resume_file
        return False

    def save_resume_file(self):
        self.resume_file = self.calculate_file_hash()

    def resume_download(self):
        if self.validate_file():
            resume_path = os.join(self.save_path, self.resume_file)
            if os.path.exists(resume_path):
                with open(resume_path, "r") as f:
                    last_pos = int(f.readline().strip())
                self.downlad_file(start_pos=last_pos)
                self.save_resume_file()
                print("Download resumed successfully.")
            else:
                print("File is not valid. Starting a new download.")
