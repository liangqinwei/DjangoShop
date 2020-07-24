"""DjMxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.renderers import OpenAPIRenderer
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer

from DjMxShop import settings, views
from common.routers.readonly_router import CustomReadOnlyRouter
from goods.views import GoodsListView, GoodsListViewSet, GoodsCategoryListViews

app_name = 'home'

router = CustomReadOnlyRouter()
# router.register('goods', GoodsListViewSet, basename='goods-list')
router.register('goods/category', GoodsCategoryListViews, basename='category-list')

urlpatterns = [
    # 配置admin url
    path('admin/', admin.site.urls),
    # 配置ckeditorurl
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # 设置rest_framework urls
    path('api-auth/', include('rest_framework.urls')),
    # 设置首页路径
    path('', views.index, name="home"),

    # 未使用router

    # path('goods/', include('goods.urls', namespace='goods')),

    path('docs/', include_docs_urls(title='平台接口文档', description='docs')),

    # 使用router
    re_path('^', include((router.urls, 'goods'))),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
