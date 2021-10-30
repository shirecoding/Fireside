__all__ = ["CustomLoginForm"]

from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):

        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields["login"].widget.attrs.update(
            {
                "id": "login-email",
                "class": "form-control",
                "type": "email",
                "autocomplete": "email",
            }
        )

        self.fields["password"].widget.attrs.update(
            {
                "id": "login-password",
                "class": "form-control",
                "type": "password",
                "autocomplete": "current-password",
            }
        )
