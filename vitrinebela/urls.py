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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin



from django.contrib.auth.views import login, logout

from vitrinebela.core import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^catalogo/', include('vitrinebela.catalog.urls', namespace='catalog')),

    url(r'^registro/$', views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),




    # url(r'^api/', include(router.urls, namespace='api')),
    # url(r'^auth/', include('rest_framework.urls', namespace='auth')),

    url(r'^reserva/', include('vitrinebela.bookings.urls', namespace='booking')),
    url(r'^api/bookings/', include('vitrinebela.bookings.api.urls', namespace='booking-api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
