from django.conf.urls import url

from vitrinebela.bookings.views import list, scheduling, scheduling_edit

urlpatterns = [
    url(r'listagem/$', list, name='list'),
    url(r'agendamento/$', scheduling, name='scheduling'),
    url(r'editar/(?P<id_booking>\d+)/$', scheduling_edit, name='scheduling_edit'),
]
