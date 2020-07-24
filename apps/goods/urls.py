from django.urls import path

from goods import views

app_name = 'goods'
urlpatterns = [
    path('query', views.GoodsListView.as_view(), name='good-list'),
    path('list', views.goods_list, name='good-list'),
]
