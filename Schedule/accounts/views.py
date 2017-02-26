from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.reverse import reverse

from .models import UserProfile
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .serializers import (UserCreateSerializer,
                          UserProfileDetailSerializer,
                          UserLoginSerializer,
                          UserUpdateSerializer,
                          UserSearchSerializer,
                          UserAddGroupSerializer)
from rest_framework.generics import (RetrieveAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser,
                                        AllowAny)
from rest_framework.response import Response
# Create your views here.


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserProfileDetailAPIView(RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'user_stu_id'

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserUpdateSerializer
    lookup_field = 'user_stu_id'
    queryset = UserProfile.objects.all()


'''
    search for user via username
    haven't put in url yet
'''

class UserSearchAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSearchSerializer
    search_fields = ['username']
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset_list = User.objects.all()
        query = self.request.GET.get("search")
        if query:
            queryset_list = queryset_list.filter(Q(username__icontains=query))
        return queryset_list


# add group


class UserAddGroupAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    # serializer_class = UserAddGroupSerializer

    def post(self, request, format=None):
        data = request.data
        current_user = self.request.user
        serializer = UserAddGroupSerializer(data=data)
        print data
        print serializer
        group_name = data['groups']
        join_group = Group.objects.get(name=group_name)
        if join_group.exists():
            current_user.groups.add(join_group)
            print "11111"
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"message": "cannot find the group"})


@api_view(['GET'])
def add_group2(request, username, group_id):
    user = User.objects.get(username=username)
    group = Group.objects.get(id=group_id)
    user.groups.add(group)
    serializer = UserAddGroupSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)



