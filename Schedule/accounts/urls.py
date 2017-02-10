from django.conf.urls import url, include
from .views import (UserCreateAPIView,
                    UserProfileDetailAPIView,
                    UserLoginAPIView,
                    UserUpdateAPIView)

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^(?P<user_stu_id>\d+)/$', UserProfileDetailAPIView.as_view(), name='profile_detail'),
    url(r'^(?P<user_stu_id>\d+)/update$', UserUpdateAPIView.as_view(), name='update')
]
