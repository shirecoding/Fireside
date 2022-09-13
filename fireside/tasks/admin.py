from django.contrib import admin
from tasks.models import Task, TaskDefinition
from fireside.admin import ModelAdmin


class TaskAdmin(ModelAdmin):
    list_display = ["name", "definition", "cron", "repeat"]
    readonly_fields = ["is_active"]

    fieldsets = [
        [None, {"fields": ("name", "description")}],
        ["Schedule", {"fields": ("cron", "repeat")}],
        ["Definition", {"fields": ("definition", "inputs")}],
        ["Activation", {"fields": ("is_active", "activate_on", "deactivate_on")}],
    ]


class TaskDefinitionAdmin(ModelAdmin):
    """
    Use `tasks.utils.register_task` to register tasks
    """

    list_display = ["name", "fpath", "description"]
    readonly_fields = ["name", "fpath", "description"]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDefinition, TaskDefinitionAdmin)
