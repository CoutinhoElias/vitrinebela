# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('django_ajax.views',
    url(r'^login/$', 'login', name='ajax_login'),
    url(r'^logout/$', 'logout', name='ajax_logout'),
)
