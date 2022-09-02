__all__ = ["Model"]

from django.db.models.base import ModelBase
from django.db import models
from django.db.models import Field
from itertools import chain
from typing import Literal
from typing import get_args
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models.query_utils import DeferredAttribute
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from django.contrib.auth.models import User, Group

FIELD_OPERATIONS_T = Literal["read", "write"]
FIELD_OPERATIONS = set(get_args(FIELD_OPERATIONS_T))


class FieldPermissionsMetaClass(ModelBase):
    """
    Adds read and write field permissions

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
                        f"write_{klas._meta.model_name}_{f.name}",
                        f"Can write {klas._meta.verbose_name} [{f.name}]",
                    ),
                    (
                        f"read_{klas._meta.model_name}_{f.name}",
                        f"Can read {klas._meta.verbose_name} [{f.name}]",
                    ),
                )

        return klas


class Model(models.Model, metaclass=FieldPermissionsMetaClass):
    """
    This `abstract` model adds extra features to the default model such as:
        - UID
        - Field level permissions

    Use with fireside.admin.ModelAdmin to access these extra features

    TODO:
        Add created_by for OLP
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
