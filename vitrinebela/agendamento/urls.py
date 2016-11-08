from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.agendamento, name='agendamento'),
    url(r'^all_events/', views.all_events, name='all_events'),
    # url(r'^admin/', include(admin.site.urls)),
]
