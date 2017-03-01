from django.conf.urls import url, include
from .views import (GroupListAPIView,
                    GroupCreateAPIView,
                    AgendaListAPIView,
                    AgendaDetailAPIView,
                    AgendaCreateAPIView, AgendaPostAPIView, agenda_create, AgendaRefreshAPIView)

urlpatterns = [
    url(r'^group/$', GroupListAPIView.as_view(), name="group_list"),
    url(r'^group/create/$', GroupCreateAPIView.as_view(), name="group_create"),
    url(r'agenda-list/$', AgendaListAPIView.as_view(), name="agenda_list"),
    url(r'^(?P<group_id>\d+)/(?P<pk>\d+)/$', AgendaDetailAPIView.as_view(), name='agenda_detail'),
    # url(r'^create/$', AgendaCreateAPIView.as_view(), name='agenda_create'),
    # url(r'^(?P<group_id>\d+)/post/$', AgendaPostAPIView.as_view(), name='agenda_create'),
    url(r'^(?P<group_id>\d+)/post/$', agenda_create, name='agenda_create'),
    url(r'^(?P<group_id>\d+)/(?P<pk>\d+)/refresh/$', AgendaRefreshAPIView.as_view(), name='agenda_refresh')
]
