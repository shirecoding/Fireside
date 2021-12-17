__all__ = ["UserProfileForm"]

from django.forms import ModelForm, Textarea

from user_profile.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["about"]
        widgets = {
            "about": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell me about yourself!",
                }
            )
        }
