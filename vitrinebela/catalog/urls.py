# coding=utf-8

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.produtct_list, name='product_list'),
    url(r'^(?P<slug>[\w_-]+)/$', views.category_list, name='category_list'),
    url(r'^produto/(?P<slug>[\w_-]+)/$', views.product, name='product'),
]