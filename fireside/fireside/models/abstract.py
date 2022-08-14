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
    """
    Adds 2 new `field` level permissions (`change_{model}_{field}`, `view_{model}_{field}`) for each `field` in the model

    Make sure to update permissions by running:

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

    TODO:
        - Add unit tests, documentation for has/assign/remove field permissions
        - has/assign/remove_field_perm should auto add the model name
            eg. (Room.has_field_perm(user, 'change'))
    """

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def has_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ) -> bool:
        assert operation in FIELD_OPERATIONS
        return user_or_group.has_perm(
            f"{operation}_{self._meta.model_name}_{field}", self
        )

    def assign_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ):
        assert operation in FIELD_OPERATIONS
        assign_perm(f"{operation}_{self._meta.model_name}_{field}", user_or_group, self)

    def remove_field_perm(
        self, user_or_group: User | Group, operation: FIELD_OPERATIONS_T, field: Field
    ):
        assert operation in FIELD_OPERATIONS
        remove_perm(f"{operation}_{self._meta.model_name}_{field}", user_or_group, self)
