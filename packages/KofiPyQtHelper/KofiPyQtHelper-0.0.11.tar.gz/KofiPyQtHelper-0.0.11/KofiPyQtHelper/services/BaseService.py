#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-04 09:45:40
LastEditors  : Kofi
LastEditTime : 2023-08-04 09:45:41
Description  : 
"""
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class BaseService:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def execute_transaction(self, func):
        try:
            with self.session.begin():
                return func()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(e)
            raise e
