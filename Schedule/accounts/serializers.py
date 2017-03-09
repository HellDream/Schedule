from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
# from rest_framework_jwt.compat import PasswordField
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
from tasks.models import Task
from .models import UserProfile
from django.contrib.auth.models import User, Permission
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        return attrs

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get('email')
        user_queryset = User.objects.filter(email=email)
        if user_queryset.exists():
            raise ValidationError("This email has been register.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        content_type = ContentType.objects.get_for_model(Task)
        permission_to_add = Permission.objects.get(codename="add_task",
                                               content_type=content_type)
        permission_to_change = Permission.objects.get(codename="change_task",
                                               content_type=content_type)
        permission_to_delete = Permission.objects.get(codename="delete_task",
                                               content_type=content_type)
        user_obj.user_permissions.add(permission_to_add,permission_to_change,permission_to_delete)
        print "succeed create a user"
        return user_obj


class UserSearchSerializer(ModelSerializer):
    """
    search for user registered
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class UserProfileDetailSerializer(ModelSerializer):
    username = SerializerMethodField()
    email = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'url',
            'username',
            'email',
            'user_stu_id',
            'school',
        ]

    def get_username(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail",kwargs={"user_stu_id": obj.user_stu_id})


class UserLoginSerializer(ModelSerializer):
    token = CharField(read_only=True,allow_blank=True)
    username = CharField()
    # password = PasswordField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

        def validate(self, data):
            return data


class UserUpdateSerializer(ModelSerializer):
    """
    Serializer to update user profile
    """
    username = SerializerMethodField()
    email = SerializerMethodField()

    class Meta:
        model = UserProfile

        fields = [
            'username',
            'email',
            'user_stu_id',
            'school',
        ]
        read_only_fields = [
            'username',
            'email',
        ]

    def get_username(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return str(obj.user.email)


class UserAddGroupSerializer(ModelSerializer):
    """
    Serializer to add and remove group.
    """
    class Meta:
        model = User
        fields = [
            'groups',
        ]


