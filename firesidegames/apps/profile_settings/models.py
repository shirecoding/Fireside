from django.db import models
import django.contrib.auth
from games.models import Game
from django.utils import timezone

from profile_settings.utils import Constants


class UserProfileSettings(models.Model):
    """
    Notes:
        - Create and link UserProfileSettings during user registration (see signals/handlers.py)
    """

    class Meta:
        verbose_name_plural = "user profile settings"

    about = models.TextField(max_length=4096, default="")
    title = models.CharField(max_length=256, default=Constants.UserTitles.initiate)
    user = models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    settings = models.JSONField(
        default=dict, help_text="User profile settings in JSON or YAML format."
    )
    games = models.ManyToManyField(Game, through="GameMembership")
    connections = models.ManyToManyField("self", through="UserConnection")
    color_theme = models.CharField(
        max_length=16,
        default=Constants.ColorTheme.p1_darkblue,
        choices=(
            (v, k)
            for k, v in Constants.ColorTheme.__dict__.items()
            if not k.startswith("__")
        ),
    )
    mail = models.ManyToManyField("Mail")

    def __str__(self):
        return f"{self.user.email}"


class GameMembership(models.Model):
    profile = models.ForeignKey(
        UserProfileSettings, related_name="game_memberships", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game, related_name="game_memberships", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime the user created an account for the game.",
    )
    last_updated = models.DateTimeField(
        default=timezone.now, help_text="The last datetime the user played the game."
    )

    def __str__(self):
        return f"{self.game}_{self.profile}"


class UserConnection(models.Model):
    user_profile = models.ForeignKey(
        UserProfileSettings, related_name="user_connections", on_delete=models.CASCADE
    )
    other_profile = models.ForeignKey(UserProfileSettings, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime this connection was created.",
    )
    connection_type = models.CharField(
        default=Constants.UserConnectionType.friend,
        choices=(
            (v, v)
            for k, v in Constants.UserConnectionType.__dict__.items()
            if not k.startswith("__")
        ),
        max_length=256,
        help_text="Type of the connection (Friend, ...)",
    )
    connection_state = models.CharField(
        default=Constants.UserConnectionState.request,
        choices=(
            (v, v)
            for k, v in Constants.UserConnectionState.__dict__.items()
            if not k.startswith("__")
        ),
        max_length=256,
        help_text="State of the connection (Accepted, Request, ...)",
    )

    def __str__(self):
        return f"{self.user_profile}_{self.other_profile}"


class Mail(models.Model):
    user_profile = models.ForeignKey(
        UserProfileSettings,
        related_name="received_mail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    from_user = models.ForeignKey(
        django.contrib.auth.get_user_model(),
        related_name="sent_mail",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime this mail was created.",
    )
    title = models.CharField(max_length=128, default="")
    content = models.TextField(max_length=4096, default="")

    def __str__(self):
        return f"{self.from_user}_{self.title}"
