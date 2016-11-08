from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_events/', views.all_events, name='all_events'),
    # url(r'^admin/', include(admin.site.urls)),
]
