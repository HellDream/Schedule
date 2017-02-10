from django.shortcuts import render
from .models import UserProfile
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import (UserCreateSerializer,
                          UserProfileDetailSerializer,
                          UserLoginSerializer,
                          UserUpdateSerializer)
from rest_framework.generics import (RetrieveAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView)
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
    queryset = UserProfile.objects.all()
    lookup_field = 'user_stu_id'
    # def get_queryset(self):
    #     queryset = User.objects.filter(user=self.request.user)
    #     return queryset


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

