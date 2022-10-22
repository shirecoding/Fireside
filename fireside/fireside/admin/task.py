from django.contrib import admin
from fireside.models import TaskSchedule, Task
from fireside.admin import ModelAdmin
from django.contrib import messages


@admin.action(description="Run selected tasks immediately")
def run_tasks(modeladmin, request, qs):
    if qs:
        jobs = [t.delay() for t in qs]
        messages.add_message(request, messages.INFO, f"Queued {jobs} for running")


class TaskScheduleAdmin(ModelAdmin):
    list_display = ["name", "description", "is_active", "priority", "timeout"]
    readonly_fields = ["is_active"]
    actions = [run_tasks]

    fieldsets = [
        [None, {"fields": ("name", "description")}],
        ["Schedule", {"fields": ("cron", "repeat", "priority")}],
        ["Definition", {"fields": ("task", "inputs")}],
        ["Activation", {"fields": ("is_active", "activate_on", "deactivate_on")}],
    ]


class TaskAdmin(ModelAdmin):
    """
    Use `fireside.utils.task.task` to register a Task
    """

    list_display = ["name", "description", "fpath", "is_valid", "priority", "timeout"]
    readonly_fields = [
        "name",
        "description",
        "fpath",
        "is_valid",
        "priority",
        "timeout",
    ]


admin.site.register(TaskSchedule, TaskScheduleAdmin)
admin.site.register(Task, TaskAdmin)
