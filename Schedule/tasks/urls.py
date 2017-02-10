from django.conf.urls import url, include
from .views import (TaskListAPIView,
                    TaskDetailAPIView,
                    TaskCreateAPIView,
                    TaskUpdateAPIView,
                    TaskDeleteAPIView)
urlpatterns = [
    url(r'^$', TaskListAPIView.as_view(), name='list'),
    url(r'^create/$', TaskCreateAPIView.as_view(), name='create'),
    url(r'^(?P<title>\w+)/$', TaskDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<title>\w+)/edit$', TaskUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<title>\w+)/delete$', TaskDeleteAPIView.as_view(), name='delete'),
]