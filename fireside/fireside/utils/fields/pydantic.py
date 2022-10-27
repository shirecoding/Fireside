__all__ = ["PydanticField"]

from django.db import models
from django.core.exceptions import ValidationError

from pydantic import BaseModel


class PydanticField(models.JSONField):
    """
    This `abstract` JSONField adds extra validation using pydantic.

    TODO:
        - write test cases
    """

    description = "Django JSONField with pydantic validation"

    pydantic_model: BaseModel

    def __init__(self, pydantic_model: BaseModel, *args, **kwargs):
        self.pydantic_model = pydantic_model
        super(PydanticField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # To bypass migration checking as pydantic_model is a required field
        if "pydantic_model" not in kwargs:
            kwargs["pydantic_model"] = None

        return name, path, args, kwargs

    def validate(self, value, model_instance):
        # check json validity
        super().validate(value, model_instance)

        # check against pydantic
        try:
            self.pydantic_model.parse_obj(value)
        except Exception as e:
            raise ValidationError(e)
