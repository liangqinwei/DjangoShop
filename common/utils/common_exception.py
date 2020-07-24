# -*- encoding: utf-8 -*-
"""
@File    : common_exception.py
@Time    : 2020-7-18 3:38
@Author  : liangqw
@Software: PyCharm
@Desc   : 自定义异常处理，需要在settion.py文件rest_framework配置此handler
"""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = []

        if response.status_code == 404:
            try:
                if not response.data.get('message'):
                    response.data['message'] = response.data.pop('detail')
                    response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            if not response.data.get('message'):
                response.data['message'] = 'Input error'

        elif response.status_code == 401:
            if not response.data.get('message'):
                response.data['message'] = "Auth failed"

        elif response.status_code >= 500:
            if not response.data.get('message'):
                response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            if not response.data.get('message'):
                response.data['message'] = "Access denied"

        elif response.status_code == 405:
            if not response.data.get('message'):
                response.data['message'] = 'Request method error'
    return response
