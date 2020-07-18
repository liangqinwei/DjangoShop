# -*- encoding: utf-8 -*-
"""
@File    : common_response.py
@Time    : 2020-7-18 2:46
@Author  : liangqw
@Software: PyCharm
@Desc   : 自定义返回response
"""
import six
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from common.constants.response_code import ResponseCode


class JsonResponse(Response):
    """
        An HttpResponse that allows its data to be rendered into
        arbitrary media types.
        """

    def __init__(self, data=None, code=None, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "message": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


# 定义success返回结构体
def Response_Success(data, msg='Success', headers=None):
    if msg:
        return JsonResponse(code=ResponseCode.SUCCESS.getCode(), msg=msg, status=status.HTTP_200_OK, data=data,
                            headers=headers)
    return JsonResponse(code=ResponseCode.SUCCESS.getCode(), msg=ResponseCode.SUCCESS.getMsg(),
                        status=status.HTTP_200_OK, data=data,
                        headers=headers)


def Response_Fails(data, msg='Fails', headers=None):
    if msg:
        return JsonResponse(code=ResponseCode.FAILS.getCode(), msg=msg, status=status.HTTP_400_BAD_REQUEST, data=data,
                            headers=headers)

    return JsonResponse(code=ResponseCode.FAILS.getCode(), msg=ResponseCode.FAILS.getMsg(),
                        status=status.HTTP_400_BAD_REQUEST, data=data,
                        headers=headers)


def Response_ServerError(data, msg='Internet server error', headers=None):
    if msg:
        return JsonResponse(code=ResponseCode.SERVERERROR.getCode(), msg=msg,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data=data,
                            headers=headers)

    return JsonResponse(code=ResponseCode.SERVERERROR.getCode(), msg=ResponseCode.SERVERERROR.getMsg(),
                        status=status.HTTP_400_BAD_REQUEST, data=data,
                        headers=headers)


def Response_NotFound(data, msg='Not found', headers=None):
    if msg:
        return JsonResponse(code=ResponseCode.NOTFOUND.getCode(), msg=msg, status=status.HTTP_404_NOT_FOUND,
                            data=data,
                            headers=headers)

    return JsonResponse(code=ResponseCode.NOTFOUND.getCode(), msg=ResponseCode.NOTFOUND.getMsg(),
                        status=status.HTTP_400_BAD_REQUEST, data=data,
                        headers=headers)


def Responses(code, data, msg, headers=None):

    return JsonResponse(code=code, msg=msg, status=status.HTTP_200_OK, data=data,
                        headers=headers)
