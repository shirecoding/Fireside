__all__ = ["CustomSignupForm"]

from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "id": "signup-email",
                "class": "form-control",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "id": "signup-password1",
                "class": "form-control",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "id": "signup-password2",
                "class": "form-control",
            }
        )
