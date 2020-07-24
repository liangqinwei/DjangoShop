from abc import ABC

from rest_framework import serializers

from goods.models import Goods, GoodsCategory


# 实现商品序列化
class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


# 实现商品只返回指定字段序列化
class GoodsPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = (
            'id', 'goods_sn', 'name', 'click_num', 'sold_num', 'fav_num', 'goods_num', 'category_id', 'shop_price',
            'goods_brief')


# 设置请求body校验
class GoodsGetDetailByNameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False,
                                 error_messages={'required': '名字不能为空'})


# 实现商品类型序列化三级
class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'
