from django.urls import reverse_lazy

from .models import Task
from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from accounts.serializers import UserProfileDetailSerializer
task_detail_url = HyperlinkedIdentityField(
        view_name='tasks:detail',
        lookup_field='title'
    )


class TaskListSerializer(ModelSerializer):
    url = task_detail_url
    delete_url = HyperlinkedIdentityField(
        view_name='tasks:delete',
        lookup_field='title'
    )
    user = SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'url',
            'delete_url',
            'id',
            'user',
            'title',
            'start_time',
            'end_time',
        ]

    def get_user(self,obj):
        return str(obj.user.username)


class TaskDetailSerializer(ModelSerializer):
    url = task_detail_url
    user = SerializerMethodField()
    user_profile = UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'url',
            'id',
            'user',
            'user_profile',
            'title',
            'detail',
            'start_time',
            'end_time',
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class TaskCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'title',
            'detail',
            'start_time',
            'end_time',
        ]
