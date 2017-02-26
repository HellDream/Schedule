# from django.shortcuts import render
from .serializers import TaskListSerializer,TaskDetailSerializer,TaskCreateUpdateSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from .models import Task
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .permissions import MyIsAuthenticated
# Create your views here.


class TaskListAPIView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'title'

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    # def get_queryset(self, *args, **kwargs):
    #     user = self.request.user
    #     username = user.username
    #     user_obj = User.objects.filter(username="qwert")
    #     # user_obj = User.objects.filter(username=username)
    #     queryset = Task.objects.filter(user=user_obj)
    #     return queryset


class TaskDetailAPIView(RetrieveAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'title'

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset


class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskCreateUpdateSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    """
        About create views: there are some issue about POST.
        Do about it later.
    """
    # def get_queryset(self, *args, **kwargs):
    #     user = self.request.user
    #     username = user.username
    #     # user_obj = User.objects.filter(username="qwert")
    #     user_obj = User.objects.filter(username=username)
    #     queryset = Task.objects.filter(user=user_obj)
    #     return queryset
    #
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     username = user.username
    #     user_obj = User.objects.filter(username=username)
    #     serializer.save(user=user_obj)


class TaskUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = TaskCreateUpdateSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    lookup_field = 'title'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset


class TaskDeleteAPIView(DestroyAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [MyIsAuthenticated]
    lookup_field = 'title'

    def get_queryset(self,*args,**kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset



