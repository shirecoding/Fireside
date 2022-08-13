__all__ = ["HorizontalFilterField"]

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField
from toolz import dissoc


class HorizontalFilterField(ModelMultipleChoiceField):
    def __init__(self, name, *args, **kwargs):
        super().__init__(
            *args,
            widget=FilteredSelectMultiple(name, is_stacked=False),
            **dissoc(kwargs, "widget")
        )
