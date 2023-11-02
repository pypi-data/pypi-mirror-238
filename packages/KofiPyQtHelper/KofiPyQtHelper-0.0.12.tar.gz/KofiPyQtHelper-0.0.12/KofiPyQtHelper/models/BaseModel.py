#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-03 11:50:20
LastEditors  : Kofi
LastEditTime : 2023-08-03 11:50:22
Description  : 
"""

import uuid, datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
