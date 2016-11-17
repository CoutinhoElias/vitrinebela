from django.conf.urls import url
from django.contrib import admin

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$',PostDetailAPIView.as_view(),name='detail'),
    url(r'^(?P<pk>\d+)/delete/$',PostDeleteAPIView.as_view(),name='delete'),
    url(r'^(?P<pk>\d+)/edit/$',PostUpdateAPIView.as_view(),name='update'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    #url(r'^(?P<slug>[\W-]+)/$',PostDetailAPIView.as_view(),name='detail')
]