# coding=utf-8

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.produtct_list, name='product_list'),
]