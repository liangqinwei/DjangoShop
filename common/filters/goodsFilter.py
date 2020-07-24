# -*- encoding: utf-8 -*-
"""
@File    : goodsByIdFilter.py
@Time    : 2020-7-21 2:42
@Author  : liangqw
@Software: PyCharm
@Desc   : 定制查询filter
"""
from django_filters import FilterSet

from goods.models import Goods


class GoodsByNameFilter(FilterSet):
    class Meta():
        model = Goods
        filters = ['id', 'name']
