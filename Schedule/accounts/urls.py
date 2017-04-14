from django.conf.urls import url, include
from .views import (UserCreateAPIView,
                    UserProfileDetailAPIView,
                    UserProfileCreateAPIView,
                    UserLoginAPIView,
                    UserUpdateAPIView,
                    UserAddGroupAPIView,
                    add_group2,
                    UserSearchAPIView,
                    RemoveGroupAPIView,
                    check_username,
                    LoadPictureAPIView,
                    is_login_view
                    )

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^profile-create/$', UserProfileCreateAPIView.as_view(), name='profile-create'),
    url(r'^profile-detail/$', UserProfileDetailAPIView.as_view(), name='profile_detail'),
    url(r'^profile-detail/update$', UserUpdateAPIView.as_view(), name='update'),
    url(r'^list/$', UserSearchAPIView.as_view(), name='user_search'),
    url(r'^(?P<group_id>\d+)/remove-group/$', RemoveGroupAPIView.as_view(), name='remove_group'),
    url(r'^(?P<group_id>\d+)/add-group/$', UserAddGroupAPIView.as_view(), name='add_group'),
    url(r'^(?P<username>\w+)/check-username/$', check_username, name="check_username"),
    url(r'(?P<username>\w+)/load-picture/$', LoadPictureAPIView.as_view(), name="load_picture"),
    url(r'is-login/$', is_login_view, name="is_login")
    # url(r'^add-group/(?P<username>\w+)/(?P<group_id>\d+)/$', add_group2, name='add_group'),
    # url(r'^remove-group/(?P<group_id>\d+)/$', remove_from_group, name='remove_from_group'),
]
