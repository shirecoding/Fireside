__all__ = ["create_settings_form"]

from django import forms


def create_settings_form(settings):
    """
    Creates a form by introspecting a settings dictionary

    settings:

        Game:
          full_screen:
            display: Full Screen
            value: true
          high_quality:
            display: High Quality
            value: false
    """

    def _populate_fields(settings):
        fields = {}
        for section, section_settings in settings.items():
            for key, kwargs in section_settings.items():
                if isinstance(kwargs["value"], bool):
                    fields[f"{section}_{key}"] = forms.BooleanField(
                        label=kwargs["display"],
                        initial=kwargs["value"],
                        required=kwargs.get("required", False),
                        widget=forms.CheckboxInput(
                            attrs={
                                "class": "form-check-input ms-auto",
                                "type": "checkbox",
                            }
                        ),
                    )
                elif isinstance(kwargs["value"], str):
                    fields[f"{section}_{key}"] = forms.CharField(
                        label=kwargs["display"],
                        initial=kwargs["value"],
                        required=kwargs.get("required", False),
                        widget=forms.TextInput(attrs={"class": "form-control"}),
                    )
        return fields

    class _SettingsForm(forms.Form):
        def __init__(self, data, *args, **kwargs):
            """
            Updates settings from request.POST
            """
            super().__init__(data, *args, **kwargs)
            if data is not None and self.is_valid():
                for section, section_settings in self.settings.items():
                    for key in section_settings:
                        section_key = f"{section}_{key}"
                        if section_key in self.cleaned_data:
                            section_settings[key]["value"] = self.cleaned_data[
                                section_key
                            ]

    return type(
        "SettingsForm",
        (_SettingsForm,),
        {"settings": settings, **_populate_fields(settings)},
    )
