from rest_framework import serializers

from goods.models import Goods


# 实现商品序列化
class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
