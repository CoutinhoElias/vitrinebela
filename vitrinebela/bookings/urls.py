from django.conf.urls import url

from vitrinebela.bookings.views import list, list_date


urlpatterns = [
    url(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/$', list_date, name='dateaaaa'),
    url(r'$', list, name='list'),
]
