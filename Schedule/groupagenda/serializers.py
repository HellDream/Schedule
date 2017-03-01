from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, DateTimeField
from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField,
                                        CharField)
from django.contrib.auth.models import Group, ContentType, Permission
from .models import Agenda, PassUser


class AgendaListSerializer(ModelSerializer):
    group = SerializerMethodField()

    class Meta:
        model = Agenda
        fields =[
            'id',
            'group',
            'title',
            'start_time',
            'end_time',
            'has_pass',
            'pass_number',
        ]

    def get_group(self, obj):
        return str(obj.group.name)


class AgendaDetailSerializer(ModelSerializer):
    group = SerializerMethodField()

    class Meta:
        model = Agenda
        fields =[
            'id',
            'group',
            'title',
            'detail',
            'start_time',
            'end_time',
            'has_pass',
            'pass_number',
        ]

    def get_group(self, obj):
        return str(obj.group.name)


class AgendaRefreshSerializer(ModelSerializer):
    # group = SerializerMethodField()

    class Meta:
        model = Agenda
        fields=[
            # 'group',
            'has_pass',
            'pass_number',
        ]

    def get_group(self, obj):
        return str(obj.group.name)


class AgendaCreateSerializer(ModelSerializer):
    # group = SerializerMethodField()
    class Meta:
        model = Agenda
        fields = [
            'title',
            'detail',
            'start_time',
            'end_time',
            'group',
        ]



class GroupCreateSerializer(ModelSerializer):
    name = CharField(label="group name")

    class Meta:
        model = Group
        fields = [
            'name'
        ]

    def validate_name(self, data):
        initial_data = self.get_initial()
        name = initial_data.get('name')
        group_qs = Group.objects.filter(name=name)
        if group_qs.exists():
            raise ValidationError("This group name has been created")
        return data

    def create(self, validated_data):
        name = validated_data['name']
        group_obj = Group(name=name)
        group_obj.save()
        content_type = ContentType.objects.get_for_model(Agenda)
        permission = Permission.objects.create(codename=name,
                                               content_type=content_type)
        group_obj.permissions.add(permission)
        print "succeed"
        return group_obj


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
        ]


class GroupDetailSerializer(ModelSerializer):
    agenda = SerializerMethodField()
    class Meta:
        model = PassUser
        fields = [
            'name',
            'agenda',
        ]

    def get_agenda(self, obj):
        return str(obj.agenda.title)




