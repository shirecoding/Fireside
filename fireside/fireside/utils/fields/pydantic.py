__all__ = ["PydanticField"]
import json

from django.core.exceptions import ValidationError
from django.db import models
from pydantic import BaseModel

from fireside.utils import JSONObject, import_path_to_function
from fireside.utils.widgets import PydanticFormField


class PydanticField(models.JSONField):
    """
    This `abstract` JSONField adds extra validation using pydantic.
    TODO:
        - write test cases
    """

    description = "Django JSONField with pydantic validation"

    def _json_to_pydantic(self, value: JSONObject) -> BaseModel:
        json_data = json.loads(value) if isinstance(value, str) else value

        klass: str = json_data.get("klass")
        assert klass is not None, "klass must be provided."

        pydantic_model: BaseModel = import_path_to_function(klass)
        return pydantic_model.parse_obj(json_data)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return self._json_to_pydantic(
            super().from_db_value(value, expression, connection)
        )

    def validate(self, value, model_instance):
        # check json validity
        super().validate(value, model_instance)

        # check against pydantic
        try:
            self._json_to_pydantic(value)
        except Exception as e:
            raise ValidationError(e)

    def formfield(self, **kwargs):
        defaults = {"form_class": PydanticFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
