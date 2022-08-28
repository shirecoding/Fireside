__all__ = ["ModelAdmin"]

from guardian.admin import GuardedModelAdmin
from fireside.models import Model
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from django.contrib import admin
from itertools import chain

shield_svg = static("fireside/img/fa-shield-halved.svg")
shield_svg_style = "float: right; height: 1em; filter: invert(45%) sepia(82%) saturate(724%) hue-rotate(154deg) brightness(95%) contrast(103%);"


class ModelAdmin(GuardedModelAdmin):
    """
    To be used with fireside.models.Model
        - Adds object level permissions (groups, users) via django-guardian
        - Handle field level permissions (requires the model to be instance of fireside.Model)

    For non superusers:
        fireside.ModelAdmin takes over the declaration of `fields` and `readonly_fields` automatically via field level permissions of the user.

    For superuser:
        `fields` and `readonly_fields` behaves as per usual
    """

    save_on_top = True

    def get_list_display(self, request, *args, **kwargs):
        return ["olp"] + super().get_list_display(request, *args, **kwargs)

    def get_list_display_links(self, request, list_display, *args, **kwargs):
        return super().get_list_display_links(
            request, list_display[1:], *args, **kwargs
        )  # skip olp

    def get_fields(self, request, obj=None) -> tuple[str] | list[str]:
        """
        For field level permissions, show if write == True || read == True
        """
        fields = super().get_fields(request, obj)

        if request.user.is_superuser:
            return fields

        # field level permissions
        return [
            f
            for f in fields
            if request.user.has_perm(
                f"{obj._meta.app_label}.read_{obj._meta.model_name}_{f}"
            )
            or request.user.has_perm(
                f"{obj._meta.app_label}.write_{obj._meta.model_name}_{f}"
            )
        ] + self.readonly_fields

        return fields

    def get_readonly_fields(
        self, request, obj: Model | None = None
    ) -> tuple[str] | list[str]:
        """
        For field level permissions, readonly if write == True && read == False
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.is_superuser:
            return readonly_fields

        # field level permissions
        return [
            f.name
            for f in chain(obj._meta.fields, obj._meta.many_to_many)
            if f.editable
            and request.user.has_perm(
                f'{obj._meta.app_label}.{obj.get_field_permission_codename(f, "read")}'
            )
            and not request.user.has_perm(
                f'{obj._meta.app_label}.{obj.get_field_permission_codename(f, "write")}'
            )
        ] + readonly_fields

    @admin.display(description="")
    def olp(self, obj: Model):
        """
        Link to object level permissions admin page
        """
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" style="{}"></a>',
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_permissions",
                args=[obj.uid],
            ),
            shield_svg,
            shield_svg_style,
        )
