from django.contrib import admin
from rest_framework.authtoken.models import Token

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
                    'school',
                    'user_stu_id']
    list_display_links = ['user_stu_id']
    list_filter = ['user','school','user_stu_id']

admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.

