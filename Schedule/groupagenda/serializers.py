from rest_framework.exceptions import ValidationError
from rest_framework.fields import ImageField
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        CharField)
from django.contrib.auth.models import Group, ContentType, Permission, User
from .utils import get_count
from .models import Agenda, PassUser, GroupProfile


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
            # 'group',
        ]


class GroupProfileDetailSerializer(ModelSerializer):
    group = SerializerMethodField()

    class Meta:
        model = GroupProfile
        fields = [
            'group',
            'description',
            'picture',
        ]

    def get_group(self, obj):
        return obj.group.name

    def get_picture(self, obj):
        try:
            picture = obj.picture.url
        except:
            picture = None
        return picture


class GroupProfileUpdateSerializer(ModelSerializer):
    picture = ImageField(use_url=True, allow_empty_file=True, allow_null=True)
    group = SerializerMethodField()

    class Meta:
        model = GroupProfile
        fields = [
            'group',
            'description',
            'picture',
        ]

    def get_group(self, obj):
        return obj.group.name

    def get_picture(self, obj):
        try:
            picture = obj.picture.url
        except:
            picture = None
        return picture


class GroupCreateSerializer(ModelSerializer):
    """To create a group with certain permissions"""
    name = CharField(label="group name")
    group_profile = GroupProfileDetailSerializer(write_only=True)
    profile = GroupProfileDetailSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'name',
            'group_profile',
            'profile',
        ]

    def validate_name(self, data):
        initial_data = self.get_initial()
        name = initial_data.get('name')
        group_qs = Group.objects.filter(name=name)
        if group_qs.exists():
            raise ValidationError("This group name has been created")
        return data

    def create_group_profile(self, group_obj, profile_data):
        description = profile_data['description']
        group_profile = GroupProfile(group=group_obj, description=description)
        group_profile.save()

    def create(self, validated_data):
        name = validated_data['name']
        group_obj = Group(name=name)
        group_obj.save()
        content_type = ContentType.objects.get_for_model(Agenda)
        permission = Permission.objects.create(codename=name,
                                               content_type=content_type)
        add_permission = Permission.objects.get(codename="change_agenda",
                                                content_type=content_type)
        delete_permission = Permission.objects.get(codename="delete_agenda",
                                                   content_type=content_type)
        group_obj.permissions.add(permission,
                                  add_permission,
                                  delete_permission)
        self.create_group_profile(group_obj, validated_data['group_profile'])
        print "succeed"
        return group_obj


class GroupListSerializer(ModelSerializer):
    member = SerializerMethodField()
    users = SerializerMethodField()
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'member',
            'users',
        ]

    def get_member(self, obj):
        group = obj.name
        quantity = User.objects.filter(groups__name=group).count()
        return quantity

    def get_users(self, obj):
        group_name = obj.name
        users = User.objects.filter(groups__name=group_name)
        user_list = []
        for user in users:
            user_list.append(user.username)
        return user_list


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


class NumberInGroupSerializer(ModelSerializer):
    """ Serializer of the number in the group with """
    first_day = SerializerMethodField()
    second_day = SerializerMethodField()
    third_day = SerializerMethodField()
    fourth_day = SerializerMethodField()
    fifth_day = SerializerMethodField()
    sixth_day = SerializerMethodField()
    seventh_day = SerializerMethodField()
    # six_to_eight = SerializerMethodField()
    class Meta:
        model = Group
        fields = [
            'name',
            'first_day',
            'second_day',
            'third_day',
            'fourth_day',
            'fifth_day',
            'sixth_day',
            'seventh_day',
            # 'six_to_eight',
        ]

    def get_first_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 0), '8:00-10:00': get_count(obj, 8, 0),
                    '10:00-12:00': get_count(obj, 10, 0), '12:00-14:00': get_count(obj, 12, 0),
                    '14:00-16:00': get_count(obj, 14, 0), '16:00-18:00': get_count(obj, 16, 0),
                    '18:00-20:00': get_count(obj, 18, 0), '20:00-22:00': get_count(obj, 20, 0)}
        return day_dict

    def get_second_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 1), '8:00-10:00': get_count(obj, 8, 1),
                    '10:00-12:00': get_count(obj, 10, 1), '12:00-14:00': get_count(obj, 12, 1),
                    '14:00-16:00': get_count(obj, 14, 1), '16:00-18:00': get_count(obj, 16, 1),
                    '18:00-20:00': get_count(obj, 18, 1), '20:00-22:00': get_count(obj, 20, 1)}
        return day_dict

    def get_third_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 2), '8:00-10:00': get_count(obj, 8, 2),
                          '10:00-12:00': get_count(obj, 10, 2), '12:00-14:00': get_count(obj, 12, 2),
                          '14:00-16:00': get_count(obj, 14, 2), '16:00-18:00': get_count(obj, 16, 2),
                          '18:00-20:00': get_count(obj, 18, 2), '20:00-22:00': get_count(obj, 20, 2)}
        return day_dict

    def get_fourth_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 3), '8:00-10:00': get_count(obj, 8, 3),
                          '10:00-12:00': get_count(obj, 10, 3), '12:00-14:00': get_count(obj, 12, 3),
                          '14:00-16:00': get_count(obj, 14, 3), '16:00-18:00': get_count(obj, 16, 3),
                          '18:00-20:00': get_count(obj, 18, 3), '20:00-22:00': get_count(obj, 20, 3)}
        return day_dict

    def get_fifth_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 4), '8:00-10:00': get_count(obj, 8, 4),
                          '10:00-12:00': get_count(obj, 10, 4), '12:00-14:00': get_count(obj, 12, 4),
                          '14:00-16:00': get_count(obj, 14, 4), '16:00-18:00': get_count(obj, 16, 4),
                          '18:00-20:00': get_count(obj, 18, 4), '20:00-22:00': get_count(obj, 20, 4)}
        return day_dict

    def get_sixth_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 5), '8:00-10:00': get_count(obj, 8, 5),
                    '10:00-12:00': get_count(obj, 10, 5), '12:00-14:00': get_count(obj, 12, 5),
                    '14:00-16:00': get_count(obj, 14, 5), '16:00-18:00': get_count(obj, 16, 5),
                    '18:00-20:00': get_count(obj, 18, 5), '20:00-22:00': get_count(obj, 20, 5)}
        return day_dict

    def get_seventh_day(self, obj):
        day_dict = {'6:00-8:00': get_count(obj, 6, 6), '8:00-10:00': get_count(obj, 8, 6),
                          '10:00-12:00': get_count(obj, 10, 6), '12:00-14:00': get_count(obj, 12, 6),
                          '14:00-16:00': get_count(obj, 14, 6), '16:00-18:00': get_count(obj, 16, 6),
                          '18:00-20:00': get_count(obj, 18, 6), '20:00-22:00': get_count(obj, 20, 6)}
        return day_dict







