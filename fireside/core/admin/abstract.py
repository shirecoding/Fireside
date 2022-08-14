__all__ = ["ModelAdmin"]

from guardian.admin import GuardedModelAdmin
from core.models import Model
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from django.contrib import admin

shield_svg = static("fireside/img/fa-shield-halved.svg")
shield_svg_style = "float: right; height: 1em; filter: invert(45%) sepia(82%) saturate(724%) hue-rotate(154deg) brightness(95%) contrast(103%);"


class ModelAdmin(GuardedModelAdmin):
    """
    To be used with core.models.Model

    - Adds object level permissions (groups, users) via django-guardian
    - Handle field level permissions (requires the model to be instance of core.Model)

    TODO:
        - Restrict for all fields not only readonly
    """

    save_on_top = True

    def get_list_display(self, request, *args, **kwargs):
        return ["olp"] + super().get_list_display(request, *args, **kwargs)

    def get_list_display_links(self, request, list_display, *args, **kwargs):
        return super().get_list_display_links(
            request, list_display[1:], *args, **kwargs
        )  # skip olp

    def get_readonly_fields(
        self, request, obj: Model | None = None
    ) -> tuple[str] | list[str]:
        if obj:
            fields = super().get_readonly_fields(request, obj)
            if request.user.is_superuser:
                return fields
            else:
                return tuple(
                    f
                    for f in fields
                    if hasattr(obj, f)
                    and (
                        obj.has_field_perm(request.user, "view", getattr(obj, f))
                        or obj.has_field_perm(request.user, "change", getattr(obj, f))
                    )
                )
        return self.readonly_fields

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
