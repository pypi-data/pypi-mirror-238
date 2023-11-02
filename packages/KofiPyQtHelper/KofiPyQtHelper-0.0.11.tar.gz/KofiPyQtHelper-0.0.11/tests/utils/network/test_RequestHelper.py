#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-02 09:35:54
LastEditors  : Kofi
LastEditTime : 2023-08-02 09:35:55
Description  : 
"""

from KofiPyQtHelper.utils.test.KofiTestCase import KofiTestCase, handleException
from KofiPyQtHelper.utils.network.RequestHelper import RequestHelper
from KofiPyQtHelper.enums.HttpEnums import RequestMethod, InterceptorsType


class RequestHelperTest(KofiTestCase):
    def setUp(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.httpClient = RequestHelper()
        self.httpClient.set_base_url(self.base_url)

    @handleException
    def test_get_request(self):
        response = self.httpClient.request("/posts/1", method=RequestMethod.Get)
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["userId"], 1)

    @handleException
    def test_post_request(self):
        response = self.httpClient.post(
            "/posts",
            json={"title": "foo", "body": "bar", "userId": 1},
        )
        self.assertEqual(response.status_code, 201)

    @handleException
    def test_put_request(self):
        data = {"title": "foo", "body": "bar", "userId": 1}
        response = self.httpClient.put("/posts/1", json=data)
        self.assertEqual(response.status_code, 200)

    @handleException
    def test_patch_request(self):
        # 更新数据
        updated_data = {"title": "foo"}
        response = self.httpClient.patch("/posts/1", json=updated_data)
        self.assertEqual(response.status_code, 200)

    @handleException
    def test_delete_request(self):
        response = self.httpClient.delete("/posts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    @handleException
    def test_head_request(self):
        response = self.httpClient.head("/posts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "")

    @handleException
    def test_request_interceptor(self):
        def request_interceptor(request_data):
            request_data["headers"]["Custom-Header"] = "Custom-Value"
            return request_data

        self.httpClient.add_interceptor(InterceptorsType.Request, request_interceptor)

        response = self.httpClient.get("/posts/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Custom-Header", response.request.headers)
        self.assertEqual(response.request.headers["Custom-Header"], "Custom-Value")

    @handleException
    def test_response_interceptor(self):
        def response_interceptor(response):
            response._content = b"Modified Response Content"
            return response

        self.httpClient.add_interceptor(InterceptorsType.Response, response_interceptor)

        response = self.httpClient.get("/posts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Modified Response Content")
