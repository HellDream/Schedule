from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from rest_framework.fields import BooleanField, NullBooleanField
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from tasks.models import Task
from .models import UserProfile
from django.contrib.auth.models import User, Permission
from rest_framework.serializers import (
    CharField,
    EmailField,
    ImageField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)


class UserProfileDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    email = SerializerMethodField()
    picture = ImageField(use_url=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'real_name',
            'description',
            'email',
            'user_stu_id',
            'school',
            'picture',
            'phone_number',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_picture(self, obj):
        try:
            picture = obj.picture.url
        except:
            picture = None
        return picture


class UserUpdateSerializer(ModelSerializer):
    """
    Serializer to update user profile
    """
    user = SerializerMethodField()
    email = SerializerMethodField()
    picture = ImageField(use_url=True, allow_empty_file=True, allow_null=True)

    class Meta:
        model = UserProfile

        fields = [
            'user',
            'real_name',
            'email',
            'description',
            'user_stu_id',
            'phone_number',
            'school',
            'picture',
        ]
        read_only_fields = [
            'user',
            'email',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_picture(self, obj):
        try:
            picture = obj.picture.url
        except:
            picture = None
        return picture


class UserProfileCreateSerializer(ModelSerializer):
    user = SerializerMethodField()
    # email = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user',
            # 'email',
            'user_stu_id',
            'real_name',
            'description',
            'phone_number',
            'school',
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    password = CharField(label='Password',
                         write_only=True,
                         style={'input_type': 'password'})
    password_confirm = CharField(label='Confirm Password',
                                 write_only=True,
                                 style={'input_type':'password'})
    user_profile = UserProfileCreateSerializer(write_only=True)
    profile = UserProfileCreateSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'user_profile',
            'profile',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        del attrs['password_confirm']
        return attrs

    def validate_password_confirm(self, value):
        data = self.get_initial()
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("The password is not confirmed")
        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get('email')
        user_queryset = User.objects.filter(email=email)
        if user_queryset.exists():
            raise ValidationError("This email has been registered.")
        return value

    def validate_username(self, value):
        data = self.get_initial()
        username = data.get('username')
        if len(username) < 9:
            raise ValidationError("The username must be more than 9 digits.")
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("The username has been registered.")
        return value

    def create_user_profile(self,user_obj , profile_data):
        nickname = profile_data['real_name']
        student_id = profile_data['user_stu_id']
        school = profile_data['school']
        user_profile = UserProfile(user=user_obj,
                                   nickname=nickname,
                                   user_stu_id=student_id,
                                   school=school)
        user_profile.save()

    def create(self, validated_data):
        print validated_data
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username,
                        email=email)
        user_obj.set_password(password)
        user_obj.save()
        # user_obj.is_active = False
        content_type = ContentType.objects.get_for_model(Task)
        permission_to_add = Permission.objects.get(codename="add_task",
                                                   content_type=content_type)
        permission_to_change = Permission.objects.get(codename="change_task",
                                                      content_type=content_type)
        permission_to_delete = Permission.objects.get(codename="delete_task",
                                                      content_type=content_type)
        user_obj.user_permissions.add(permission_to_add, permission_to_change, permission_to_delete)
        print "succeed create a user"
        self.create_user_profile(user_obj, validated_data['user_profile'])
        return user_obj


class UserSearchSerializer(ModelSerializer):
    """
    search for user registered
    """
    picture = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'picture',
        ]

    def get_picture(self, obj):
        username = obj.username
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            try:
                 picture = user_profile.picture.url
            except:
                picture = None
            return picture
        except User.DoesNotExist:
            return None
        except UserProfile.DoesNotExist:
            return None


class UserLoginSerializer(ModelSerializer):
    token = CharField(read_only=True, allow_blank=True)
    username = CharField()
    remembered = BooleanField(write_only=True, required=False)
    password = CharField(style={'input_type': 'password'})
    picture = SerializerMethodField(read_only=True)

    # password = PasswordField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
            'remembered',
            'picture',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

        def validate(self, data):
            return data

    def get_picture(self, obj):
        username = obj['username']
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            try:
                picture = user_profile.picture.url
            except:
                picture = None
            return picture
        except User.DoesNotExist:
            return None
        except UserProfile.DoesNotExist:
            return None


class LoadUserPictureSerializer(ModelSerializer):
    picture = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'picture'
        ]

    def get_picture(self, obj):
        return obj.picture.url


class UserAddGroupSerializer(ModelSerializer):
    """
    Serializer to add and remove group.
    """

    class Meta:
        model = User
        fields = [
            'groups',
        ]


