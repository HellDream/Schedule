from django.conf.urls import url, include
from .views import (UserCreateAPIView,
                    UserProfileDetailAPIView,
                    UserLoginAPIView,
                    UserUpdateAPIView,
                    UserAddGroupAPIView,
                    UserSearchAPIView,
                    add_group2,
                    # remove_from_group,
                    RemoveGroupAPIView)

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^(?P<user_stu_id>\d+)/$', UserProfileDetailAPIView.as_view(), name='profile_detail'),
    url(r'^(?P<user_stu_id>\d+)/update$', UserUpdateAPIView.as_view(), name='update'),
    url(r'^list/$', UserSearchAPIView.as_view(), name='user_search'),
    url(r'^(?P<group_id>\d+)/remove-group/$', RemoveGroupAPIView.as_view(), name='remove_group'),
    url(r'^(?P<group_id>\d+)/add-group/$', UserAddGroupAPIView.as_view(), name='add_group'),
    # url(r'^add-group/(?P<username>\w+)/(?P<group_id>\d+)/$', add_group2, name='add_group'),
    # url(r'^remove-group/(?P<group_id>\d+)/$', remove_from_group, name='remove_from_group'),
]
