from django.urls import reverse_lazy

from .models import Task
from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from django.utils import timezone
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
    is_past = SerializerMethodField()
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
            'is_past',
        ]

    def get_user(self,obj):
        return str(obj.user.username)

    def get_is_past(self, obj):
        now = timezone.now()
        if now <= obj.end_time:
            return False
        elif now > obj.end_time:
            return True


class TaskDetailSerializer(ModelSerializer):
    url = task_detail_url
    user = SerializerMethodField()
    # user_profile = SerializerMethodField()
    is_past = SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'url',
            'id',
            'user',
            'title',
            'detail',
            'start_time',
            'end_time',
            'is_past',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_is_past(self, obj):
        now = timezone.now()
        if now <= obj.end_time:
            return False
        elif now > obj.end_time:
            return True



class TaskCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'title',
            'detail',
            'start_time',
            'end_time',
        ]
