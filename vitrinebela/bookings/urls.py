from django.conf.urls import url

from vitrinebela.bookings.views import list, scheduling

urlpatterns = [
    url(r'listagem/$', list, name='list'),
    url(r'agendamento/$', scheduling, name='scheduling'),
]
