# -*- encoding: utf-8 -*-
"""
@File    : error_middleWare.py
@Time    : 2020-7-19 0:08
@Author  : liangqw
@Software: PyCharm
@Desc   : 全局异常中间件捕获
"""
import json
import logging
import traceback
from collections import OrderedDict

from django.http import HttpResponse, HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from common.constants.response_code import ResponseCode
from common.utils.common_response import JsonResponse

logger = logging.getLogger('default')


class ExceptionErrorMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        """
        处理请求过程中异常
        :param request:
        :param exception:
        :return:
        """
        logger.error("异常堆栈 ", exc_info=traceback.format_exc())
        # return JsonResponse(code=ResponseCode.UNKNOWN_ERROR.getCode(), msg=ResponseCode.UNKNOWN_ERROR.getMsg(),
        #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="")

        return HttpResponse(json.dumps({"code": 500, "data": "", "msg": "未知异常"}))

    def process_request(self, request):
        """
        处理请求路径不存在，请求前异常
        :param request:
        :return:
        """
        # todo(可以进行权限控制，访问白名单，是否登入等认证)
        # 获取访问的url
        current_url = request.path_info

        # return HttpResponse(json.dumps({"code": 500, "data": "", "msg": "未知异常"}))

    def process_response(self, request, response):
        """
        处理请求过程中异常
        :param request:
        :param exception:
        :return:
        """

        code = response.status_code

        # HttpResponseNotFound异常处理，在process_exception中不知道为什么捕获不到，特殊处理
        if code == 404 and isinstance(response, HttpResponseNotFound):
            logger.error("HttpResponseNotFound异常堆栈", exc_info=traceback.format_exc())
            return HttpResponse(json.dumps({"code": 404, "data": "", "msg": "Resource not found"}))

        return response
