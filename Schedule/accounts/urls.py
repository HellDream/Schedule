from django.conf.urls import url, include
from .views import (UserCreateAPIView,
                    UserProfileDetailAPIView,
                    UserLoginAPIView,
                    UserUpdateAPIView,
                    UserAddGroupAPIView,
                    UserSearchAPIView,
                    add_group2)

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^(?P<user_stu_id>\d+)/$', UserProfileDetailAPIView.as_view(), name='profile_detail'),
    url(r'^(?P<user_stu_id>\d+)/update$', UserUpdateAPIView.as_view(), name='update'),
    url(r'^add-group/(?P<user_id>\d+)/$', UserAddGroupAPIView.as_view(), name='add_group'),
    url(r'^add-group-2/(?P<username>\w+)/(?P<group_id>\d+)/$', add_group2, name='add_group2'),
    url(r'^list/$', UserSearchAPIView.as_view(), name='user_search')
]
