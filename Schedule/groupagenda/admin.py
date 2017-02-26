from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Agenda, PassUser


class AgendaModelAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "end_time", "has_pass", "pass_number"]
    list_display_links = ["title"]
    search_fields = ["title"]

    class Meta:
        model = Agenda


class PassUserModelAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
    search_fields = ["name"]

    class Meta:
        model = PassUser

admin.site.register(Permission)
admin.site.register(Agenda, AgendaModelAdmin)
admin.site.register(PassUser, PassUserModelAdmin)

# Register your models here.
