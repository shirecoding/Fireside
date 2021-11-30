__all__ = ["YAMLWidget"]

import json
import yaml

from django.forms.widgets import Textarea


class YAMLWidget(Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        style = attrs.get("style")
        font_family = "font-family: monospace; height: 260px"
        style = f"{style}; {font_family}" if style else font_family
        attrs["style"] = style

        return super().render(name, value, attrs=attrs, renderer=renderer)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)

        if value.strip() in ["", "---"]:
            return "{}"

        d = yaml.safe_load(value)

        return json.dumps(d)

    def format_value(self, value):
        d = None if value is None else json.loads(value)

        if not d:
            if isinstance(d, list):
                return "[]"
            elif isinstance(d, dict):
                return r"{}"

        return str(
            yaml.safe_dump(
                d, default_flow_style=False, explicit_start=True, allow_unicode=True
            )
        )
