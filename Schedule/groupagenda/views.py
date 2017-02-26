from django.db.models import Q
from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Agenda, PassUser
from .serializers import (AgendaListSerializer,
                          AgendaDetailSerializer,
                          AgendaCreateSerializer,
                          GroupCreateSerializer,
                          GroupListSerializer)
from rest_framework.generics import (RetrieveAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser,
                                        AllowAny)
from django.contrib.auth.models import User, Group


class AgendaListAPIView(ListAPIView):
    serializer_class = AgendaListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        for group in self.get_current_group():
            queryset = Agenda.objects.filter(group=group)
            print type(queryset)
            queryset_list.append(queryset)
        return queryset_list

    def get_current_group(self):
        current_group_set = Group.objects.filter(user=self.request.user)
        return current_group_set


class AgendaDetailAPIView(RetrieveAPIView):
    serializer_class = AgendaDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        current_group = Group.objects.get(user=self.request.user)
        queryset = Agenda.objects.filter(group=current_group)
        return queryset


class AgendaCreateAPIViev(CreateAPIView):
    serializer_class = AgendaCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        current_group = Group.objects.get(user=self.request.user)
        queryset = Agenda.objects.filter(group=current_group)
        return queryset

    def perform_create(self, serializer):
        current_group = Group.objects.get(user=self.request.user)
        serializer.save(group=current_group)


class GroupCreateAPIView(CreateAPIView):
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        queryset = Group.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        data = serializer.data
        print data
        name = data['name']
        created_group = Group.objects.get(name=name)
        user.groups.add(created_group)

'''
    Here to show all the group and search for the group via name
'''
class GroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Group.objects.all()
        query = self.request.GET.get("search")
        if query:
            queryset_list = queryset_list.filter(Q(name__icontains=query))
        return queryset_list








