from django.contrib import admin
from fireside.models import Task, TaskDefinition
from fireside.admin import ModelAdmin
from django.contrib import messages


@admin.action(description="Run selected tasks immediately")
def run_tasks(modeladmin, request, qs):
    if qs:
        jobs = [t.delay() for t in qs]
        messages.add_message(request, messages.INFO, f"Queued {jobs} for running")


class TaskAdmin(ModelAdmin):
    list_display = ["name", "definition", "cron", "repeat"]
    readonly_fields = ["is_active"]
    actions = [run_tasks]

    fieldsets = [
        [None, {"fields": ("name", "description")}],
        ["Schedule", {"fields": ("cron", "repeat", "priority")}],
        ["Definition", {"fields": ("definition", "inputs")}],
        ["Activation", {"fields": ("is_active", "activate_on", "deactivate_on")}],
    ]


class TaskDefinitionAdmin(ModelAdmin):
    """
    Use `fireside.utils.tasks.task` to register a TaskDefinition
    """

    list_display = ["name", "fpath", "description"]
    readonly_fields = ["name", "fpath", "description"]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDefinition, TaskDefinitionAdmin)
