# Create your views here.
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, parser_classes, permission_classes, action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.constants.response_code import ResponseCode
from common.utils.common_base_view import CustomViewBase
from common.utils.common_pagination import LargeResultsSetPagination
from common.utils.common_response import JsonResponse, Response_Success
from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerializer, GoodsGetDetailByNameSerializer, GoodsPartSerializer, \
    GoodsCategorySerializer


class GoodsListView(APIView):
    # 设置权限认证：认证
    permission_classes = (AllowAny,)

    # @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        goods = Goods.objects.all()
        pagination = LargeResultsSetPagination()
        page_goods = pagination.paginate_queryset(queryset=goods, request=request, view=self)
        goods_serializer = GoodsSerializer(instance=page_goods, many=True)
        return pagination.get_paginated_response(goods_serializer.data)

    def get(self, request, format=None):
        goods = Goods.objects.all()
        pagination = LargeResultsSetPagination()
        page_goods = pagination.paginate_queryset(queryset=goods, request=request, view=self)
        goods_serializer = GoodsSerializer(instance=page_goods, many=True)
        return pagination.get_paginated_response(goods_serializer.data)


class GoodsListViewSet(CustomViewBase):
    '商品列表页'

    queryset = Goods.objects.all().order_by('id')
    pagination_class = LargeResultsSetPagination
    serializer_class = GoodsSerializer

    # lookup_field = 'goods_sn'

    @action(methods=['get'], detail=True)
    def get_detail(self, request, pk=None):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        goods = self.get_object()
        serializer = self.get_serializer(goods)

        return Response_Success(data=serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
# 忽略认证
@permission_classes((permissions.AllowAny,))
def goods_list(request, format=None):
    goods = GoodsGetDetailByNameSerializer(data=request.data)
    if goods.is_valid():
        queryset = Goods.objects.filter(name=request.data.get('name')).all()
        goods_serializer = GoodsPartSerializer(instance=queryset, many=True)
        return Response_Success(data=goods_serializer.data)
    else:
        return JsonResponse(code=ResponseCode.FAILS.getCode(), data='', msg=goods.errors.get('name')[0])


class GoodsCategoryListViews(CustomViewBase):
    """
    商品类型信息
    """
    queryset = GoodsCategory.objects.all().filter(category_type=1)
    serializer_class = GoodsCategorySerializer
    pagination_class = LargeResultsSetPagination
