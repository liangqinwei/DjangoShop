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
from django.urls import path, include

from DjMxShop import settings, views

app_name = 'home'
urlpatterns = [
    # 配置admin url
    path('admin/', admin.site.urls),
    # 配置ckeditorurl
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # 设置rest_framework urls
    path('api-auth/', include('rest_framework.urls')),
    # 设置首页路径
    path('', views.index, name="home"),

    path('goods/', include('goods.urls', namespace='goods'))

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
