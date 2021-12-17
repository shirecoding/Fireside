__all__ = ["ReplyMailForm"]

from django.forms import ModelForm, Textarea, TextInput, CharField, HiddenInput

from user_profile.models import Mail


class ReplyMailForm(ModelForm):

    mail_id = CharField(widget=HiddenInput())  # the mail being replied to
    reply_to = CharField(  # user name being replied to (for display only)
        widget=TextInput(attrs={"class": "form-control", "readonly": True})
    )

    class Meta:
        model = Mail
        fields = ["reply_to", "title", "content", "mail_id"]
        labels = {"reply_to": "Reply to"}
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,  # when replying, the title is hardcoded to 'Re: {title}'
                }
            ),
            "content": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }
