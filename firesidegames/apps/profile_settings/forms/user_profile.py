__all__ = ["UserProfileForm"]

from django.forms import ModelForm, Textarea

from profile_settings.models import UserProfileSettings


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfileSettings
        fields = ["about"]
        widgets = {
            "about": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell me about yourself!",
                }
            )
        }
