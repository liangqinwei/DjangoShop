# -*- encoding: utf-8 -*-
"""
@File    : response_code.py
@Time    : 2020-7-18 16:15
@Author  : liangqw
@Software: PyCharm
@Desc   : 返回状态码枚举类
"""
from enum import Enum, unique


@unique
class ResponseCode(Enum):
    SUCCESS = {200: 'Success'}
    FAILS = {400: 'Bad request'}
    NOTFOUND = {404: 'not found'}
    AUTH_FAILED = {401: 'Auth failed'}
    DENIED = {403: 'Access denied'}
    SERVERERROR = {500: 'Internet server error'}
    LOGIN_FAILED = {200101: '登录失败'}
    UNKNOWN_ERROR = {200100: '未知异常'}

    def getCode(self):
        return list(self.value.keys())[0]

    def getMsg(self):
        return list(self.value.values())[0]


if __name__ == '__main__':
    t = ResponseCode.SUCCESS.getMsg()
    print(t)
