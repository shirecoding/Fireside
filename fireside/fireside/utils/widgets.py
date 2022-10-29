__all__ = ["DynamicHelpTextInput"]

from django.forms.widgets import TextInput


class DynamicHelpTextInput(TextInput):
    template_name = "fireside/widgets/dynamic_help_text_input.html"
