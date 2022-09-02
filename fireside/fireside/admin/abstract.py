__all__ = ["ModelAdmin"]

from guardian.admin import GuardedModelAdmin
from fireside.models import Model
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from django.contrib import admin
from itertools import chain
from django.contrib.auth import get_permission_codename
from guardian.shortcuts import get_objects_for_user, get_perms_for_model

shield_svg = static("fireside/img/fa-shield-halved.svg")
shield_svg_style = "float: right; height: 1em; filter: invert(45%) sepia(82%) saturate(724%) hue-rotate(154deg) brightness(95%) contrast(103%);"


class ModelAdmin(GuardedModelAdmin):
    """
    To be used with fireside.models.Model, adds the following:

        MLP (Module Level Permissions)
        OLP (Object Level Permissions)
        FLP (Field Level Permissions)

    [change, view, delete] behaviour:
        - OLP = True and MLP = False   =>   User can only operate on his instances
        - MLP = True                   =>   User can operate on all instances

    [add] behaviour:
        - MLP = True                   =>   User can add new instances

    [module] behaviour:
        - MLP = True or OLP = True     =>   User can view module in admin

    For superusers:
        - Additional shortcuts list field is provided
        - `fields` and `readonly_fields` behaves as per usual

    For non superusers:
        fireside.ModelAdmin takes over the declaration of `fields` and `readonly_fields` automatically via field level permissions of the user.
    """

    save_on_top = True

    def permission_from_op(self, op: str):
        return f"{self.opts.app_label}.{get_permission_codename(op, self.opts)}"

    def get_user_objects(
        self, request, perms: list[str] | str = "", any_perm: bool = False
    ):
        return get_objects_for_user(
            request.user,
            perms or get_perms_for_model(self.model).values_list("codename", flat=True),
            klass=self.model,
            any_perm=any_perm,
        )

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_module_permission(self, request):
        return (
            super().has_module_permission(request)
            or self.get_user_objects(request, any_perm=True).exists()
        )

    def get_queryset(self, request):
        if super().has_view_permission(request) or super().has_change_permission(
            request
        ):
            return super().get_queryset(request)
        return self.get_user_objects(
            request,
            perms=[
                self.permission_from_op("change"),
                self.permission_from_op("view"),
                self.permission_from_op("delete"),
            ],
        )

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return (
                super().has_view_permission(request)
                or self.get_user_objects(
                    request, perms=self.permission_from_op("change")
                ).exists()
            )
        return super().has_change_permission(request, obj) or request.user.has_perm(
            self.permission_from_op("change"), obj
        )

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return (
                super().has_view_permission(request)
                or self.get_user_objects(
                    request, perms=self.permission_from_op("delete")
                ).exists()
            )
        return super().has_delete_permission(request, obj) or request.user.has_perm(
            self.permission_from_op("delete"), obj
        )

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return (
                super().has_view_permission(request)
                or self.get_user_objects(
                    request, perms=self.permission_from_op("view")
                ).exists()
            )
        return super().has_view_permission(request, obj) or request.user.has_perm(
            self.permission_from_op("view"), obj
        )

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

    def get_list_display(self, request, *args, **kwargs):
        return ["shortcuts"] + super().get_list_display(request, *args, **kwargs)

    def get_list_display_links(self, request, list_display, *args, **kwargs):
        return super().get_list_display_links(
            request, list_display[1:], *args, **kwargs
        )  # offset shortcuts

    @admin.display(description="")
    def shortcuts(self, obj: Model):
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
