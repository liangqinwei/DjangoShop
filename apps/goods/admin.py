from django.contrib import admin

# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline

from goods.models import GoodsCategory, Goods, GoodsImage, Banner, HotSearchWords


class GoodsImagesInline(GenericTabularInline):
    model = GoodsImage
    exclude = ["create_time"]
    extra = 1
    style = 'table'


# 继承admin.ModelAdmin ,注入GoodsAdmin才成功
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'goods_sn', 'goods_num', 'market_price', 'shop_price', 'click_num'
        , 'sold_num', 'is_hot', 'is_new', 'create_time', 'update_time']
    list_display_links = ['name']
    search_fields = ['name', 'code', 'category_type']
    list_filter = ['category']
    # 设置列表内可以编辑
    list_editable = ['is_hot', 'is_new']
    style_fields = {'goods_desc', 'ueditor'}
    # 日期过滤
    date_hierarchy = 'create_time'

    inlines = [GoodsImagesInline]


class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'desc', 'category_type', 'parent_category', 'is_tab', "create_time",
                    'update_time']
    list_display_links = ['name']
    search_fields = ['name', 'code', 'category_type']
    list_filter = ['category_type']
    list_editable = ['is_tab']
    date_hierarchy = 'create_time'


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'content_type', 'object_id', 'content_object', "create_time", 'update_time']
    search_fields = ['image']
    # list_filter = ['image']


class HotSearchWordsAdmin(admin.ModelAdmin):
    list_display = ['id', 'keywords', 'index', "create_time", 'update_time']
    search_fields = ['keywords']
    # list_filter = ['keywords']


class BannersAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'image', 'index', "create_time", 'update_time']
    search_fields = ['goods']
    list_filter = ['goods']
    list_editable = ['index']


# 注册model
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(HotSearchWords, HotSearchWordsAdmin)

admin.site.register(Banner, BannersAdmin)
