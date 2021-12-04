__all__ = ["UserProfileForm"]

from django.forms import ModelForm, TextInput

from profile_settings.models import UserProfileSettings


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfileSettings
        fields = ["about"]
        widgets = {
            "about": TextInput(
                attrs={
                    "class": "form-control",
                    # 'style': 'max-width: 300px;',
                    "placeholder": "Tell me about yourself!",
                }
            )
        }
