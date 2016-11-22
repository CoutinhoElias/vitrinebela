"""vitrinebela URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from vitrinebela.bookings.views import BookingViewSet
from vitrinebela.core import views

# router = routers.DefaultRouter()
# router.register(r'bookings', BookingViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    # url(r'^produto/$', views.product, name='product'),
    url(r'^catalogo/', include('vitrinebela.catalog.urls', namespace='catalog')),
    #url(r'^agendamentos/', include('vitrinebela.agendamento.urls', namespace='agendamento')),

    # url(r'^api/', include(router.urls, namespace='api')),
    # url(r'^auth/', include('rest_framework.urls', namespace='auth')),

    url(r'^bookings/', include('vitrinebela.bookings.urls', namespace='booking')),
    url(r'^api/bookings/', include('vitrinebela.bookings.api.urls', namespace='booking-api')),
]
