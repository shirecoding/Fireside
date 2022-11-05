__all__ = ["HintsTextInput"]

from django.forms.widgets import TextInput


class HintsTextInput(TextInput):
    template_name = "fireside/widgets/hints_text_input.html"

    def __init__(self, hints_url: str | None = None, *args, **kwargs):
        self.hints_url = hints_url
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        return {**super().get_context(*args, **kwargs), "hints_url": self.hints_url}
