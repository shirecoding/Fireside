from django.db import models
import django.contrib.auth


class UserProfileSettings(models.Model):
    """
    Notes:
        - Create and link UserProfileSettings during user registration (see signals/handlers.py)
    """

    about = models.TextField(max_length=4096, default="")
    user = models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    settings = models.JSONField(
        default={}, help_text="User profile settings in JSON or YAML format."
    )

    def __str__(self):
        return f"{self.user.email}"
