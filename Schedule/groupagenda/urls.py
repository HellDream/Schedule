from django.conf.urls import url, include
from .views import (GroupListAPIView,
                    GroupCreateAPIView)

urlpatterns = [
    url(r'^group/$', GroupListAPIView.as_view(), name="group_list"),
    url(r'^group/create/$', GroupCreateAPIView.as_view(), name="group_create"),
]
