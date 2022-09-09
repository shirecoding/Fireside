from django.contrib import admin
from tasks.models import Task, TaskDefinition
from fireside.admin import ModelAdmin


class TaskAdmin(ModelAdmin):
    list_display = ["name", "definition"]


class TaskDefinitionAdmin(ModelAdmin):
    """
    Use `tasks.utils.register_task` to register tasks
    """

    list_display = ["name", "fpath", "description"]
    readonly_fields = ["name", "fpath", "description"]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDefinition, TaskDefinitionAdmin)
