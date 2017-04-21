import datetime

from django.conf import settings
from django.db.models import Q
from django.http.response import Http404
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FileUploadParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import (UserCreateSerializer,
                          UserProfileDetailSerializer,
                          UserLoginSerializer,
                          UserUpdateSerializer,
                          UserSearchSerializer,
                          UserAddGroupSerializer,
                          UserProfileCreateSerializer,
                          LoadUserPictureSerializer)
from rest_framework.generics import (RetrieveAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.response import Response
from .models import UserProfile
# from django.shortcuts import render
# from rest_framework.reverse import reverse
# Create your views here.


class UserProfileCreateAPIView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileDetailAPIView(ListAPIView):
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'user_stu_id'

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset


class UserUpdateAPIView(APIView):
    """
    wait for modification
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes = [FileUploadParser]

    def get_object(self):
        user = self.request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise Http404
        return user_profile

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = UserUpdateSerializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data
        user_profile = self.get_object()
        try:
            picture = user_profile.picture
            print type(picture)
        except:
            picture = None
        if data['picture'] is None and picture is not None:
            data['picture'] = picture
        print data['picture']
        serializer = UserUpdateSerializer(user_profile, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        data = request.data
        user_profile = self.get_object()
        serializer = UserUpdateSerializer(user_profile, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        response = super(UserCreateAPIView, self).post(request,*args, **kwargs)
        response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                            value=request.session.session_key,
                            expires=datetime.datetime.now())
        return response


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        data = request.data
        print request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = User.objects.get(username=new_data['username'])
            login(request, user)
            response = Response(new_data, status=HTTP_200_OK)
            if data.get('remembered'):
                if data['remembered']:
                    response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                                        value=request.session.session_key,
                                        max_age=60*43200)
            else:
                response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                                    value=request.session.session_key,
                                    expires=datetime.datetime.now())
            return response
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


class LoadPictureAPIView(APIView):
    """
    load picture without log in
    """
    permission_classes = [AllowAny]
    serializer_class = LoadUserPictureSerializer

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, *args, **kwargs):
        data = request.data
        user = self.get_user(username)
        try:
            user_profile = UserProfile.objects.get(user=user)
            serializer = LoadUserPictureSerializer(user_profile, data=data)
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data, status=HTTP_200_OK)
        except UserProfile.DoesNotExist:
            raise Http404


class UserSearchAPIView(ListAPIView):
    """
    user searching api view blur searching
    """
    permission_classes = [AllowAny]
    serializer_class = UserSearchSerializer
    # search_fields = ['username']
    # here to define where to search, which is not suitable for blur searching
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset_list = User.objects.filter(username=None)
        query = self.request.GET.get("search")
        if query:
            user_profile = UserProfile.objects.filter(Q(phone_number__icontains=query)|
                                                      Q(nickname__icontains=query)|
                                                      Q(user_stu_id__icontains=query))
            if user_profile.exists():
                for obj in user_profile:
                    print obj.user.username
                    queryset_list = queryset_list | User.objects.filter(username=obj.user.username)
            queryset_list = \
                queryset_list | User.objects.filter(
                Q(username__icontains=query)|
                Q(email__icontains=query)
            )
        return queryset_list


class UserAddGroupAPIView(APIView):
    """
    add group api
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddGroupSerializer

    def get(self, request, group_id, *args, **kwargs):
        user = self.request.user
        group = Group.objects.get(id=group_id)
        user.groups.add(group)
        serializer = UserAddGroupSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def add_group2(request, username, group_id):
    user = User.objects.get(username=username)
    group = Group.objects.get(id=group_id)
    user.groups.add(group)
    serializer = UserAddGroupSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)


class RemoveGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = UserAddGroupSerializer

    def get(self, request, group_id, *args, **kwargs):
        data = request.data
        user = self.request.user
        group = Group.objects.get(id=group_id)
        user.groups.remove(group)
        serializer = UserAddGroupSerializer(user, data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_username(request, username):
    """
    check if the username has been used.
    :param request:
    :param username:
    :return:message, code
    """
    pass_message = "the username is never used"
    error_message = "the username has been used"
    try:
        user=User.objects.filter(username=username)
    except User.DoesNotExist:
        return HTTP_400_BAD_REQUEST
    if user:
        return Response({'message':error_message,'code':0}, status=HTTP_400_BAD_REQUEST)
    return Response({'message':pass_message, 'code':1}, status=HTTP_200_OK)


@api_view(['GET'])
def is_login_view(request):
    """
    check if the user is login
    :param request:
    :return:
    """
    if request.COOKIES['sessionid']== request.session.session_key:
        return Response({'message':"the user has logged in"}, status=HTTP_200_OK)
    else:
        return Response({'message':"the user is not found"}, status=HTTP_400_BAD_REQUEST)





# @api_view(['GET'])
# def remove_from_group(request, group_id):
#     user = request.user
#     group = Group.objects.get(id=group_id)
#     user.groups.remove(group)
#     serializer = UserAddGroupSerializer(user)
#     if serializer.is_valid():
#         return Response(serializer.data, status=HTTP_200_OK)
#     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

