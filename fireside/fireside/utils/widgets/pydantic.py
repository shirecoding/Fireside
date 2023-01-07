__all__ = ["PydanticFormField"]
from django.forms.fields import JSONField
from pydantic import BaseModel


class PydanticFormField(JSONField):
    def prepare_value(self, value):
        if isinstance(value, BaseModel):
            return super().prepare_value(value.dict())
        return super().prepare_value(value)
