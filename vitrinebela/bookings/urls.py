from django.conf.urls import url

from vitrinebela.bookings import views
from vitrinebela.bookings.views import list, list_date


urlpatterns = [
    url(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/$', list_date, name='date'),
    url(r'$', list, name='list'),

    #url(r'^calendario/$', views.calendario, name='calendario'),
    url(r'^carga_eventos/$', views.cargaEventos, name="cargaEventos"),
    url(r'^crea_eventos/$', views.creaEventos, name="creaEventos"),
    url(r'^elimina_eventos/$', views.eliminaEventos, name="eliminaEventos"),
    url(r'^actualiza_visitador/$', views.actualizaVisitador, name="actualizaVisitador"),
    #url(r'^api/get_visitadores/$', views.get_visitadores, name='get_visitadores'),
]
