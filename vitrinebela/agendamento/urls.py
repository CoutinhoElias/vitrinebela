from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'agendamento.views.index', name='index'),
    url(r'^all_events/', 'agendamento.views.all_events', name='all_events'),
    # url(r'^admin/', include(admin.site.urls)),
]
