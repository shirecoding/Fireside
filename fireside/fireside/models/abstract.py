__all__ = ["Model"]

from django.db.models.base import ModelBase
from django.db import models
from django.db.models import Field
from itertools import chain
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from typing import Literal
from typing import get_args
import uuid

FIELD_OPERATIONS_T = Literal["change", "view"]
FIELD_OPERATIONS = set(get_args(FIELD_OPERATIONS_T))


class FieldPermissionsMetaClass(ModelBase):
    def __new__(cls, name, bases, attrs):
        klas = super().__new__(cls, name, bases, attrs)

        if not klas._meta.abstract:
            # Add permissions for each field (change and view ONLY)
            for f in chain(klas._meta.fields, klas._meta.many_to_many):
                klas._meta.permissions = (
                    *klas._meta.permissions,
                    (f"change[{f}]", f"Can change {f.name}"),
                    (f"view[{f}]", f"Can view {f.name}"),
                )

        return klas


class Model(models.Model, metaclass=FieldPermissionsMetaClass):
    """
    TODO:
        - if user, check if any of user's group has permissions
        - this is at object level, how to add perms to all instances ?? or will has_perm do it for you
    """

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def has_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ) -> bool:
        assert operation in FIELD_OPERATIONS
        return user_or_group.has_perm(f"{operation}[{field}]", self)

    def assign_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ):
        assert operation in FIELD_OPERATIONS
        assign_perm(f"{operation}[{field}]", user_or_group, self)

    def remove_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ):
        assert operation in FIELD_OPERATIONS
        remove_perm(f"{operation}[{field}]", user_or_group, self)
