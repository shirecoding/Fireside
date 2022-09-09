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
from functools import lru_cache
from cachetools.func import ttl_cache

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

    TODO:
        - list_display permissions
            - how to do this fast?
            - add a seperate permission for list display?
            - compiling user permissions from all objects would be slow
            - make seperate table to keep track of list_permissions and update? too tedious to keep it updated
            - or just ignore totally?
            - current it needs global change to be able edit, else its readonly

        - Add test cases for all combinations
            - global read
            - global write
            - global delete
            - global none + obj read
            - global none + obj write
            - ...

        - Try adding thousands of items and test speed of queryset
    """

    save_on_top = True

    @lru_cache
    def permission_from_op(self, op: str, field: str | None = None, include_app_label: bool = True):
        s = (
            f"{self.opts.app_label}.{get_permission_codename(op, self.opts)}"
            if include_app_label
            else get_permission_codename(op, self.opts)
        )
        if field:
            return f"{s}_{field}"
        return s

    @lru_cache
    def get_perms_for_model(self, fields: tuple[str] | None = None):
        fields = fields or tuple()
        return [
            *get_perms_for_model(self.model).values_list("codename", flat=True),
            *(self.permission_from_op("read", field=f, include_app_label=False) for f in fields),
            *(self.permission_from_op("write", field=f, include_app_label=False) for f in fields),
        ]

    def get_user_objects(self, request, perms: list[str] | str = "", any_perm: bool = False):
        fields = self.get_fields(request)
        return (
            get_objects_for_user(
                request.user,
                perms or self.get_perms_for_model(tuple(fields)),
                klass=self.model,
                any_perm=any_perm,
            )
            or self.model.objects.none()
        )

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_module_permission(self, request):
        return super().has_module_permission(request) or self.get_user_objects(request, any_perm=True).exists()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        fields = self.get_fields(request)
        if (
            super().has_view_permission(request)
            or super().has_change_permission(request)
            or any(request.user.has_perm(self.permission_from_op("read", field=f)) for f in fields)
            or any(request.user.has_perm(self.permission_from_op("write", field=f)) for f in fields)
        ):
            return queryset
        return self.get_user_objects(request, any_perm=True)

    def has_change_permission(self, request, obj=None):
        fields = self.get_fields(request, obj)
        if obj is None:
            return (
                super().has_change_permission(request)
                or self.get_user_objects(request, perms=self.permission_from_op("change")).exists()
                or any(request.user.has_perm(self.permission_from_op("write", field=f)) for f in fields)
            )
        return (
            super().has_change_permission(request, obj)
            or request.user.has_perm(self.permission_from_op("change"), obj)
            or any(request.user.has_perm(self.permission_from_op("write", field=f), obj) for f in fields)
        )

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return (
                super().has_delete_permission(request)
                or self.get_user_objects(request, perms=self.permission_from_op("delete")).exists()
            )
        return super().has_delete_permission(request, obj) or request.user.has_perm(
            self.permission_from_op("delete"), obj
        )

    def has_view_permission(self, request, obj=None):
        fields = self.get_fields(request, obj)
        if obj is None:
            return (
                super().has_view_permission(request)
                or any(request.user.has_perm(self.permission_from_op("read", field=f)) for f in fields)
                or any(request.user.has_perm(self.permission_from_op("write", field=f)) for f in fields)
                or self.get_user_objects(request, any_perm=True).exists()
            )
        return super().has_view_permission(request, obj) or fields

    @ttl_cache(ttl=10)
    def filter_fields_for_obj(self, user, obj, fields: tuple[str], readonly: bool = False) -> list[str]:
        if readonly:
            return list(
                dict.fromkeys(f for f in fields if not user.has_perm(self.permission_from_op("write", field=f), obj))
            )

        return [
            f
            for f in fields
            if user.has_perm(self.permission_from_op("view"))
            or user.has_perm(self.permission_from_op("change"))
            or user.has_perm(self.permission_from_op("read", field=f))
            or user.has_perm(self.permission_from_op("write", field=f))
            or user.has_perm(self.permission_from_op("read", field=f), obj)
            or user.has_perm(self.permission_from_op("write", field=f), obj)
        ]

    def get_fields(self, request, obj=None) -> tuple[str] | list[str]:
        fields = super().get_fields(request, obj)
        if obj is None:
            return fields

        # filter FLP
        return self.filter_fields_for_obj(request.user, obj, tuple(fields))

    def get_fieldsets(self, request, obj=None):
        fields = self.get_fields(request, obj)
        return [
            (x, {**d, "fields": fs})
            for x, d in super().get_fieldsets(request, obj)
            if (
                fs := [
                    f if isinstance(f, str) and f in fields else tuple(t for t in f if t in fields)
                    for f in d.get("fields", [])
                ]
            )
        ]

    @lru_cache
    def _editable_fields(self) -> tuple[str]:
        return [f.name for f in chain(self.opts.fields, self.opts.many_to_many) if f.editable]

    def get_readonly_fields(self, request, obj: Model | None = None) -> tuple[str] | list[str]:
        """
        FLP behaviour:
            readonly: write and !read
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.is_superuser:
            return readonly_fields

        # move fields without FLP into readonly
        fields = self.fields or self._editable_fields()
        return tuple({*readonly_fields, *self.filter_fields_for_obj(request.user, obj, tuple(fields), readonly=True)})

    def get_list_display(self, request, *args, **kwargs):
        return ["shortcuts"] + super().get_list_display(request, *args, **kwargs)

    def get_list_display_links(self, request, list_display, *args, **kwargs):
        return super().get_list_display_links(request, list_display[1:], *args, **kwargs)  # offset shortcuts

    @admin.display(description="")
    def shortcuts(self, obj: Model):
        """
        Shortcuts column
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
