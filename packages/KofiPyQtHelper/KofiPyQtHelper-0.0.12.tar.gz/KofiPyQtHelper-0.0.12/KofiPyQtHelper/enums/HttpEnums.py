"""
Author       : Kofi
Date         : 2022-07-27 19:09:23
LastEditors  : Kofi
LastEditTime : 2022-08-12 10:46:33
Description  : 请求类型
"""

from enum import Enum


class RequestMethod(Enum):
    Get = "get"
    Head = "head"
    Post = "post"
    Put = "put"
    Patch = "patch"
    Delete = "delete"


class InterceptorsType(Enum):
    Request = "request"
    Response = "response"
