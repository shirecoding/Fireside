__all__ = ["FiresideTextInput"]

from django.forms.widgets import TextInput


class FiresideTextInput(TextInput):
    template_name = "fireside/widgets/fireside_text_input.html"
    hint_callback = None

    def get_context(self, *args, **kwargs):
        return {
            **super().get_context(*args, **kwargs),
            "hint_callback": self.hint_callback,
        }
