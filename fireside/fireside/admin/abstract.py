__all__ = ["ModelAdmin"]

from guardian.admin import GuardedModelAdmin
from fireside.models import Model, ActivatableModel
from django.urls import reverse
from django.contrib import admin
from itertools import chain
from django.contrib.auth import get_permission_codename
from guardian.shortcuts import get_objects_for_user, get_perms_for_model
from functools import lru_cache
from cachetools.func import ttl_cache
from django.template.loader import render_to_string


class ModelAdmin(GuardedModelAdmin):
    """
    Used with `fireside.models.Model`, `fireside.models.ActivatableModel`.

    Adds the following:

    - OLP (Object Level Permissions)
    - FLP (Field Level Permissions)
    - MLP (Module Level Permissions, django's default permissions)

    Change, View, Delete Behaviour:

        Can operate on all instances:
            User has relevant MLP permissions

        Can only operate on user's instances:
            User has relevant OLP permissions ONLY (no MLP permissions)

    Add Behaviour:

        Can add instance:
            User has add MLP permissions

    Module Behaviour:

        Can view module:
            User has either MLP or OLP permissions

    Superuser Behaviour:

        FLP is not applicable to superusers

    Activate/Deactivate Behaviour:

        User has MLP change permissions
    """

    save_on_top = True
    actions = ["activate", "deactivate"]

    @lru_cache
    def permission_from_op(
        self, op: str, field: str | None = None, include_app_label: bool = True
    ):
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
            *(
                self.permission_from_op("view", field=f, include_app_label=False)
                for f in fields
            ),
            *(
                self.permission_from_op("change", field=f, include_app_label=False)
                for f in fields
            ),
        ]

    def get_user_objects(
        self, request, perms: list[str] | str = "", any_perm: bool = False
    ):
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        fields = self.get_fields(request)
        if (
            super().has_view_permission(request)
            or super().has_change_permission(request)
            or any(
                request.user.has_perm(self.permission_from_op("view", field=f))
                for f in fields
            )
            or any(
                request.user.has_perm(self.permission_from_op("change", field=f))
                for f in fields
            )
        ):
            return queryset
        return self.get_user_objects(request, any_perm=True)

    def has_module_permission(self, request):
        return (
            super().has_module_permission(request)
            or self.get_user_objects(request, any_perm=True).exists()
        )

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        fields = self.get_fields(request, obj)
        if obj is None:
            return (
                super().has_change_permission(request)
                or any(
                    request.user.has_perm(self.permission_from_op("change", field=f))
                    for f in fields
                )
                or self.get_user_objects(
                    request,
                    perms=[
                        self.permission_from_op("change"),
                        *(self.permission_from_op("change", field=f) for f in fields),
                    ],
                ).exists()
            )
        return (
            super().has_change_permission(request, obj)
            or request.user.has_perm(self.permission_from_op("change"), obj)
            or any(
                request.user.has_perm(self.permission_from_op("change", field=f))
                for f in fields
            )
            or any(
                request.user.has_perm(self.permission_from_op("change", field=f), obj)
                for f in fields
            )
        )

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return (
                super().has_delete_permission(request)
                or self.get_user_objects(
                    request, perms=self.permission_from_op("delete")
                ).exists()
            )
        return super().has_delete_permission(request, obj) or request.user.has_perm(
            self.permission_from_op("delete"), obj
        )

    def has_view_permission(self, request, obj=None):
        fields = self.get_fields(request, obj)
        if obj is None:
            return (
                super().has_view_permission(request)
                or any(
                    request.user.has_perm(self.permission_from_op("view", field=f))
                    for f in fields
                )
                or any(
                    request.user.has_perm(self.permission_from_op("change", field=f))
                    for f in fields
                )
                or self.get_user_objects(request, any_perm=True).exists()
            )
        return super().has_view_permission(request, obj) or fields

    @ttl_cache(ttl=10)
    def filter_fields_for_obj(
        self, user, obj, fields: tuple[str], readonly: bool = False
    ) -> list[str]:
        if readonly:
            return list(
                dict.fromkeys(
                    f
                    for f in fields
                    if not user.has_perm(self.permission_from_op("change"))
                    and not user.has_perm(self.permission_from_op("change", field=f))
                    and not user.has_perm(
                        self.permission_from_op("change", field=f), obj
                    )
                )
            )

        return [
            f
            for f in fields
            if user.has_perm(self.permission_from_op("view"))
            or user.has_perm(self.permission_from_op("change"))
            or user.has_perm(self.permission_from_op("view", field=f))
            or user.has_perm(self.permission_from_op("change", field=f))
            or user.has_perm(self.permission_from_op("view", field=f), obj)
            or user.has_perm(self.permission_from_op("change", field=f), obj)
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
                    f
                    if isinstance(f, str) and f in fields
                    else tuple(t for t in f if t in fields)
                    for f in d.get("fields", [])
                ]
            )
        ]

    @lru_cache
    def _editable_fields(self) -> tuple[str]:
        return [
            f.name
            for f in chain(self.opts.fields, self.opts.many_to_many)
            if f.editable
        ]

    def get_readonly_fields(
        self, request, obj: Model | None = None
    ) -> tuple[str] | list[str]:
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.is_superuser:
            return readonly_fields

        # move fields without FLP into readonly
        fields = self.fields or self._editable_fields()
        return tuple(
            {
                *readonly_fields,
                *self.filter_fields_for_obj(
                    request.user, obj, tuple(fields), readonly=True
                ),
            }
        )

    def get_list_display(self, request, *args, **kwargs):
        return ["shortcuts"] + super().get_list_display(request, *args, **kwargs)

    def get_list_display_links(self, request, list_display, *args, **kwargs):
        return super().get_list_display_links(
            request, list_display[1:], *args, **kwargs
        )  # offset shortcuts

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not issubclass(self.model, ActivatableModel):
            for a in ["activate", "deactivate"]:
                if a in actions:
                    del actions[a]
        return actions

    @admin.action(
        description="Activate selected task schedules", permissions=["change"]
    )
    def activate(self, request, qs):
        qs.activate()

    @admin.action(
        description="Deactivate selected task schedules", permissions=["change"]
    )
    def deactivate(self, request, qs):
        qs.deactivate()

    @admin.display(description="")
    def shortcuts(self, obj):
        """
        Shortcuts column
        """

        context = {
            "is_active": None,
            "olp_link": None,
        }

        if isinstance(obj, ActivatableModel):
            context["is_active"] = obj.is_active

        if isinstance(obj, Model):
            context["olp_link"] = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_permissions",
                args=[obj.uid],
            )

        return render_to_string("fireside/admin/shortcuts.html", context)
