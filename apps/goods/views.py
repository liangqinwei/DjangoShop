# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.common_pagination import LargeResultsSetPagination
from common.utils.common_response import JsonResponse
from goods.models import Goods
from goods.serializers import GoodsSerializer


class GoodsListView(APIView):
    # 设置权限认证：认证
    permission_classes = (AllowAny,)

    # @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        goods = Goods.objects.all()
        pagenation = LargeResultsSetPagination()
        page_goods = pagenation.paginate_queryset(queryset=goods, request=request, view=self)
        goods_serializer = GoodsSerializer(instance=page_goods, many=True)
        return pagenation.get_paginated_response(goods_serializer.data)


    def get(self, request, format=None):
        goods = Goods.objects.all()
        pagenation = LargeResultsSetPagination()
        page_goods = pagenation.paginate_queryset(queryset=goods, request=request, view=self)
        goods_serializer = GoodsSerializer(instance=page_goods, many=True)
        return pagenation.get_paginated_response(goods_serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
# 忽略认证
@permission_classes((permissions.AllowAny,))
def goods_list(request, format=None):
    return JsonResponse({'received data': request.data})
