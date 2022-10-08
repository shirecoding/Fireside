from django.contrib import admin
from fireside.models import Task, TaskDefinition
from fireside.admin import ModelAdmin


class TaskAdmin(ModelAdmin):
    list_display = ["name", "definition", "cron", "repeat"]
    readonly_fields = ["is_active"]

    fieldsets = [
        [None, {"fields": ("name", "description")}],
        ["Schedule", {"fields": ("cron", "repeat", "priority")}],
        ["Definition", {"fields": ("definition", "inputs")}],
        ["Activation", {"fields": ("is_active", "activate_on", "deactivate_on")}],
    ]


class TaskDefinitionAdmin(ModelAdmin):
    """
    Use `fireside.utils.tasks.register_task` to register tasks
    """

    list_display = ["name", "fpath", "description"]
    readonly_fields = ["name", "fpath", "description"]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDefinition, TaskDefinitionAdmin)
