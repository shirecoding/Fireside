__all__ = ["Model", "TimestampModel", "ActivatableModel"]

import uuid
from itertools import chain
from typing import Literal, get_args

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Field, Q
from django.db.models.base import ModelBase
from django.db.models.query_utils import DeferredAttribute
from django.utils import timezone
from guardian.shortcuts import assign_perm, remove_perm

FIELD_OPERATIONS_T = Literal["view", "change"]
FIELD_OPERATIONS = set(get_args(FIELD_OPERATIONS_T))


class FieldPermissionsMetaClass(ModelBase):
    """
    Adds view and change field permissions

    TODO:
        Add `can view all instances`

    Update permissions by running:
        ```
        ./manage.py update_permissions
        ./manage.py remove_stale_contenttypes
        ```
    """

    def __new__(cls, name, *args, **kwargs):
        klas = super().__new__(cls, name, *args, **kwargs)

        if not klas._meta.abstract:
            for f in chain(klas._meta.fields, klas._meta.many_to_many):
                klas._meta.permissions = (
                    *klas._meta.permissions,
                    (
                        f"change_{klas._meta.model_name}_{f.name}",
                        f"Can change {klas._meta.verbose_name} [{f.name}]",
                    ),
                    (
                        f"view_{klas._meta.model_name}_{f.name}",
                        f"Can view {klas._meta.verbose_name} [{f.name}]",
                    ),
                )

        return klas


class Model(models.Model, metaclass=FieldPermissionsMetaClass):
    """
    This `abstract` model adds extra features to the default model such as:
        - UID
        - Field level permissions

    Use with fireside.admin.ModelAdmin to access these extra features
    """

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    @classmethod
    def get_permission_by_codename(cls, codename: str) -> Permission:
        return Permission.objects.get(
            codename=codename, content_type=ContentType.objects.get_for_model(cls)
        )

    @classmethod
    def get_field_permission(
        cls, field: Field | DeferredAttribute, operation: FIELD_OPERATIONS_T
    ) -> Permission:
        return Permission.objects.get(
            codename=f"{operation}_{cls._meta.model_name}_{field.field.name if isinstance(field, DeferredAttribute) else field.name}",
            content_type=ContentType.objects.get_for_model(cls),
        )

    @classmethod
    def get_field_permission_codename(
        cls, field: Field | DeferredAttribute, operation: FIELD_OPERATIONS_T
    ) -> str:
        return f"{operation}_{cls._meta.model_name}_{field.field.name if isinstance(field, DeferredAttribute) else field.name}"

    def assign_perm(
        self, perm: Permission | str, user_or_group: User | Group
    ) -> Permission:
        """
        Assign permission to this object instance
        """
        return assign_perm(perm, user_or_group, self)

    def remove_perm(self, perm: Permission | str, user_or_group: User | Group):
        """
        Remove permission from this object instance
        """
        return remove_perm(perm, user_or_group, self)

    def has_perm(self, perm: Permission | str, user_or_group: User | Group) -> bool:
        return user_or_group.has_perm(
            ".".join(perm.natural_key()[:2][::-1])
            if isinstance(perm, Permission)
            else perm,
            self,
        )


class TimestampModel(models.Model):
    """
    TODO:
        - write test cases
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivatableModelQuerySet(models.QuerySet):
    """
    Note: save signals are not triggered on activate/deactivate queryset update
    """

    def activate(self):
        self.update(deactivate_on=None, activate_on=None)

    def deactivate(self):
        self.update(deactivate_on=timezone.now())


class ActivatableModelManager(models.Manager):
    def get_queryset(self):
        return ActivatableModelQuerySet(self.model, using=self._db)

    def is_active_query(self):
        now = timezone.now()
        return Q(activate_on__isnull=False) & (
            Q(deactivate_on__isnull=True) & Q(activate_on__lt=now)
            | Q(deactivate_on__isnull=False)
            & Q(activate_on__lt=now)
            & Q(deactivate_on__gt=now)
        ) | Q(activate_on__isnull=True) & (
            Q(deactivate_on__isnull=True) | Q(deactivate_on__gt=now)
        )

    def activated(self):
        return self.filter(self.is_active_query())

    def deactivated(self):
        return self.filter(~self.is_active_query())


class ActivatableModel(models.Model):
    """
    activate() will reset `deactivate_on` and `activate_on` to None
    deactivate() will set `deactivate_on` to the current time
    """

    activate_on = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the model is considered activated (If None, model is considered activate as long as `now` < `deactivate_on`)",
    )
    deactivate_on = models.DateTimeField(
        blank=True, null=True, help_text="When the model is considered deactivated."
    )

    objects = ActivatableModelManager()

    class Meta:
        abstract = True

    @property
    def is_active(self):
        if self.activate_on:
            if self.deactivate_on:
                return self.deactivate_on > timezone.now() > self.activate_on
            else:
                return timezone.now() > self.activate_on
        else:
            if self.deactivate_on:
                return self.deactivate_on > timezone.now()
            else:
                return True

    def deactivate(self):
        self.deactivate_on = timezone.now()
        self.save(update_fields=["deactivate_on"])

    def activate(self):
        self.deactivate_on = None
        self.activate_on = None
        self.save(update_fields=["deactivate_on", "activate_on"])
