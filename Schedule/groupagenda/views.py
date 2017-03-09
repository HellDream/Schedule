import json

from django.db.models import Q, F
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from .models import Agenda, PassUser
from .serializers import (AgendaListSerializer,
                          AgendaDetailSerializer,
                          AgendaCreateSerializer,
                          AgendaRefreshSerializer,
                          GroupCreateSerializer,
                          GroupListSerializer,
                          NumberInGroupSerializer)
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
        queryset = Agenda.objects.filter(group=None)
        for group in self.get_current_group():
            _queryset = Agenda.objects.filter(group=group)
            queryset = queryset | _queryset
        return queryset

    def get_current_group(self):
        current_group_set = Group.objects.filter(user=self.request.user)
        print current_group_set
        return current_group_set

# WRONG Detail for agenda!!!
# class AgendaDetailAPIView(RetrieveAPIView):
#     serializer_class = AgendaDetailSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#     def get_queryset(self,group_id, *args, **kwargs):
#         queryset = Agenda.objects.filter(group=None)
#         for group in self.get_current_group(group_id):
#             _queryset = Agenda.objects.filter(group=group)
#             queryset = queryset |_queryset
#         return queryset
#
#     def get_current_group(self, group_id):
#         current_group_set = Group.objects.filter(id=group_id,user=self.request.user)
#         print current_group_set
#         return current_group_set


class AgendaDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_object(self, group_id, pk):
        print group_id
        print pk
        try:
            group = Group.objects.get(id=group_id, user=self.request.user)
            return Agenda.objects.get(group=group, pk=pk)
        except Group.DoesNotExist:
            raise Http404
        except Agenda.DoesNotExist:
            raise Http404

    def get(self, request, group_id, pk, *args, **kwargs):
        agenda = self.get_object(group_id, pk)
        serializer = AgendaDetailSerializer(agenda)
        return Response(serializer.data)


'''RAW Agenda refresh to check if the agenda instance is passed'''


class AgendaRefreshAPIView(APIView):
    # need to rewrite a permission for the agenda to check if the user is in the related group
    permission_classes = [IsAuthenticated]

    def get_object(self, group_id, pk):
        print group_id
        print pk
        try:
            group = Group.objects.get(id=group_id, user=self.request.user)
            return Agenda.objects.get(group=group, pk=pk)
        except Group.DoesNotExist:
            raise Http404
        except Agenda.DoesNotExist:
            raise Http404

    def get(self, request, group_id, pk, *args, **kwargs):
        pre_agenda = self.get_object(group_id, pk)
        pre_agenda.pass_number = F('pass_number') + 1
        pre_agenda.save()
        print type(pre_agenda)
        if pre_agenda.get_pass_number() > 10:
            pre_agenda = Agenda.objects.filter(pk=pre_agenda.pk).update(has_pass=True)
        serializer = AgendaRefreshSerializer(pre_agenda)
        agenda = self.get_object(group_id, pk)
        if agenda.has_pass == True:
            serializer = AgendaDetailSerializer(agenda)
        return Response(serializer.data, status=HTTP_200_OK)

'''RAW agenda create api view'''


class AgendaCreateAPIView(CreateAPIView):
    serializer_class = AgendaCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthenticated]

    # def get_serializer_context(self):

    def get_queryset(self, *args, **kwargs):
        current_group = Group.objects.filter(user=self.request.user)
        queryset = Agenda.objects.all()
        for group in current_group:
            _queryset = queryset.filter(group=group)
            queryset = queryset | _queryset
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class AgendaPostAPIView(APIView):
    """updated agenda create api view"""
    serializer_class = AgendaCreateSerializer

    def get_object(self, group_id):
        print group_id
        try:
            group = Group.objects.get(id=group_id, user=self.request.user)
            return Agenda.objects.filter(group=group)
        except Group.DoesNotExist:
            raise Http404
        except Agenda.DoesNotExist:
            raise Http404

    def post(self, request, group_id, *args, **kwargs):
        data = request.data
        print type(data)
        title = data['title']
        detail = data['detail']
        start_time = data['start_time']
        end_time = data['end_time']
        print type(start_time)
        group = Group.objects.get(id=group_id)
        agenda = Agenda.objects.create(title=title,
                                       start_time=start_time,
                                       detail=detail,
                                       end_time=end_time,
                                       group=group)
        serializer = AgendaCreateSerializer(agenda, data=data)
        if serializer.is_valid():
            print serializer.data
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agenda_create(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        data = request.data
        title = data['title']
        detail = data['detail']
        start_time = data['start_time']
        end_time = data['end_time']
        print data
        print type(data)
        agenda = Agenda.objects.create(title=title,
                                       start_time=start_time,
                                       detail=detail,
                                       end_time=end_time,
                                       group=group)
        serializer = AgendaCreateSerializer(agenda, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GroupCreateAPIView(CreateAPIView):
    """
    the api view of creating a group
    """
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

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


class GroupListAPIView(ListAPIView):
    """
    Here to show all the group and search for the group via name
    """
    serializer_class = GroupListSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Group.objects.filter(user=self.request.user)
        query = self.request.GET.get("search")
        if query:
            queryset_list = queryset_list.filter(Q(name__iexact=query))
        return queryset_list


class NumberInGroupAPIView(RetrieveAPIView):
    serializer_class = NumberInGroupSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    queryset = Group.objects.all()
