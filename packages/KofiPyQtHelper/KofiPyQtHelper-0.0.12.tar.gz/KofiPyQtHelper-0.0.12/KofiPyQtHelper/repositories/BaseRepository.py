#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-03 14:22:04
LastEditors  : Kofi
LastEditTime : 2023-08-03 14:22:05
Description  : 
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker()


class BaseRepository:
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def add(self, model):
        try:
            self.session.add(model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def update(self, model):
        try:
            current = (
                self.session.query(self.model_class).filter_by(id=model.id).first()
            )
            if current:
                self.session.merge(model)
            else:
                self.session.add(model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get(self, **kwargs):
        return self.session.query(self.model_class).filter_by(**kwargs).first()

    def list_all(self):
        return self.session.query(self.model_class).all()

    def paginate(self, page=1, per_page=10):
        return self.session.query(self.model_class).paginate(
            page, per_page, error_out=False
        )

    def execute_query(self, query):
        return self.session.execute(query)


def transactional(fn):
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            session.begin()
            result = fn(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
