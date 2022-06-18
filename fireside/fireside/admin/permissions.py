from django.contrib.auth.models import Permission
from django.contrib import admin


class PermissionAdmin(admin.ModelAdmin):
    list_filter = ("content_type__app_label",)
    search_fields = (
        "name",
        "codename",
    )


# Add Permissions to admin
admin.site.register(Permission, PermissionAdmin)
