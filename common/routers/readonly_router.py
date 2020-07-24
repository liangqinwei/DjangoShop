# -*- encoding: utf-8 -*-
"""
@File    : readonly_router.py
@Time    : 2020-7-20 20:39
@Author  : liangqw
@Software: PyCharm
@Desc   : 自定义动态路由，只保留 list threive,屏幕put patch
"""
from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class CustomReadOnlyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
