from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Agenda, PassUser, GroupProfile


class AgendaModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "start_time", "end_time", "has_pass", "pass_number"]
    list_display_links = ["title"]
    search_fields = ["title"]

    class Meta:
        model = Agenda


class PassUserModelAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
    search_fields = ["name"]

    class Meta:
        model = PassUser


class GroupProfileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "group"]
    list_display_links = ["id"]

    class Meta:
        model = GroupProfile
admin.site.register(Permission)
admin.site.register(Agenda, AgendaModelAdmin)
admin.site.register(PassUser, PassUserModelAdmin)
admin.site.register(GroupProfile, GroupProfileModelAdmin)
# Register your models here.
