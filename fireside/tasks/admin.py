from django.contrib import admin
from tasks.models import Task
from fireside.admin import ModelAdmin


class TaskAdmin(ModelAdmin):
    list_display = ["name", "task"]


admin.site.register(Task, TaskAdmin)
