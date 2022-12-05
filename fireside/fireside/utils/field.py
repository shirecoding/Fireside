__all__ = ["get_field_name", "FIELD_OPERATIONS_T", "FIELD_OPERATIONS", "FIELD_T"]

from typing import Literal, get_args

from django.db.models import Field
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.query_utils import DeferredAttribute

FIELD_OPERATIONS_T = Literal["view", "change"]
FIELD_OPERATIONS = set(get_args(FIELD_OPERATIONS_T))
FIELD_T = Field | DeferredAttribute | ForwardManyToOneDescriptor | str


def get_field_name(f: FIELD_T) -> str:
    if isinstance(f, Field):
        return f.name
    elif isinstance(
        f,
        (
            DeferredAttribute,
            ForwardManyToOneDescriptor,
        ),
    ):
        return f.field.name
    elif isinstance(str):
        return f
