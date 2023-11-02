#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-01 08:19:56
LastEditors  : Kofi
LastEditTime : 2023-08-01 08:19:57
Description  : 
"""

import unittest


def handleException(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            args[0].fail(f"Test failed due to exception: {str(e)}")

    return wrapper


class KofiTestCase(unittest.TestCase):
    def run(self, result=None):
        self._resultForDoCleanups = result
        super().run(result)

    def addCleanup(self, function, *args, **kwargs):
        def wrapped_cleanup():
            try:
                function(*args, **kwargs)
            except Exception as e:
                self.fail(f"Test failed due to exception: {str(e)}")

        super().addCleanup(wrapped_cleanup)
