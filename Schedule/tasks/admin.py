from django.contrib import admin
from .models import Task
# Register your models here.


class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "end_time"]
    list_display_links = ["start_time"]
    list_editable = ["title"]
    search_fields = ["title"]

    class Meta:
        model = Task


admin.site.register(Task, TaskModelAdmin)