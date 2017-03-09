from django.conf.urls import url, include
from .views import (GroupListAPIView,
                    GroupCreateAPIView,
                    AgendaListAPIView,
                    AgendaDetailAPIView,
                    AgendaCreateAPIView,
                    AgendaPostAPIView,
                    agenda_create,
                    AgendaRefreshAPIView,
                    NumberInGroupAPIView)

urlpatterns = [
    url(r'^group/$', GroupListAPIView.as_view(), name="group_list"),
    url(r'^group/create/$', GroupCreateAPIView.as_view(), name="group_create"),
    url(r'agenda-list/$', AgendaListAPIView.as_view(), name="agenda_list"),
    url(r'^(?P<group_id>\d+)/(?P<pk>\d+)/$', AgendaDetailAPIView.as_view(), name='agenda_detail'),
    # url(r'^create/$', AgendaCreateAPIView.as_view(), name='agenda_create'),
    url(r'^(?P<group_id>\d+)/post2/$', AgendaPostAPIView.as_view(), name='agenda_create2'),  # recommended api
    url(r'^(?P<group_id>\d+)/post/$', agenda_create, name='agenda_create'),
    url(r'^(?P<group_id>\d+)/(?P<pk>\d+)/refresh/$', AgendaRefreshAPIView.as_view(), name='agenda_refresh'),
    url(r'^(?P<id>\d+)/number/$', NumberInGroupAPIView.as_view(), name="number")
]
