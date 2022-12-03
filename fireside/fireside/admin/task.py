from django.contrib import admin
from fireside.models import TaskSchedule, Task
from fireside.admin import ModelAdmin
from django.contrib import messages
from django.forms import ModelForm
from fireside.utils.widgets import CronTextInput


class TaskScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cron"].widget = CronTextInput()


class TaskScheduleAdmin(ModelAdmin):
    form = TaskScheduleForm
    list_display = [
        "task",
        "cron_pretty",
        "repeat",
        "description",
        "is_active",
        "priority",
        "timeout",
    ]
    readonly_fields = ["is_active"]
    actions = ModelAdmin.actions + ["run_tasks"]

    fieldsets = [
        ["Task", {"fields": ("task", "inputs")}],
        ["Schedule", {"fields": ("cron", "repeat", "priority")}],
        ["Activation", {"fields": ("is_active", "activate_on", "deactivate_on")}],
    ]

    @admin.action(description="Run selected tasks")
    def run_tasks(self, request, qs):
        if qs:
            jobs = [t.delay() for t in qs]
            messages.add_message(request, messages.INFO, f"Queued {jobs} for running")


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
