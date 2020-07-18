# -*- encoding: utf-8 -*-
"""
@File    : common_pagination.py
@Time    : 2020-7-18 3:43
@Author  : liangqw
@Software: PyCharm
@Desc   : 处定义分页
"""
from collections import OrderedDict

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response

from common.utils import common_response
from common.utils.common_response import JsonResponse


# rest_framework分页
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'page'

    def get_paginated_response(self, data):

        return common_response.Response_Success(data=OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('size', self.page.paginator.per_page),
            ('records', data),
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)

        # 为了兼容post，get传或者不传page，重写了page_number的获取方法，将原方法下一行注释
        # page_number = request.query_params.get(self.page_query_param, 1)
        page_number = self.get_page(request)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    # 重写pagination的get_page_size
    def get_page_size(self, request):
        if self.page_size_query_param:
            if request.query_params.get(self.page_size_query_param):
                sizes = request.query_params[self.page_size_query_param]
            elif request.data.get(self.page_size_query_param):
                sizes = request.data.get(self.page_size_query_param)
            else:
                return self.page_size
            try:
                return _positive_int(
                    sizes,
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page

    # 定义获取page,默认返回第1页
    def get_page(self, request):
        if self.page_query_param:
            if request.query_params.get(self.page_query_param):
                sizes = request.query_params[self.page_query_param]
            elif request.data.get(self.page_query_param):
                sizes = request.data.get(self.page_query_param)
            else:
                return 1
            try:
                return _positive_int(
                    sizes,
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return 1


# 分页，已废弃
def api_pagination(objs, request, Serializer):
    try:
        page_size = int(request.data.get('page_size', 10))
        page = int(request.data.get('page', 1))
    except(TabError, ValueError):
        return JsonResponse(code=status.HTTP_400_BAD_REQUEST, data="", msg="page and pagesize must be integer")
    paginator = Paginator(objs, page_size)
    total = paginator.num_pages
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    serializer = Serializer(objs, many=True)  # 序列化操作
    return JsonResponse(code=status.HTTP_200_OK, data=OrderedDict([
        ('page', page),
        ('pages', total),
        ('size', page_size),
        ('count', paginator.count),
        ('records', serializer.data),
    ]), msg="success")
