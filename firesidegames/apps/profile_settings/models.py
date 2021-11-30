from django.db import models
import django.contrib.auth
from games.models import Game
from datetime import datetime

DEFAULT_TITLE = "Initiate"


class UserProfileSettings(models.Model):
    """
    Notes:
        - Create and link UserProfileSettings during user registration (see signals/handlers.py)
    """

    class Meta:
        verbose_name_plural = "user profile settings"

    about = models.TextField(max_length=4096, default="")
    title = models.CharField(max_length=256, default="Initiate")
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
        default=datetime.utcnow,
        help_text="The datetime the user created an account for the game.",
    )
    last_updated = models.DateTimeField(
        default=datetime.utcnow, help_text="The last datetime the user played the game."
    )

    def __str__(self):
        return f"{self.game}_{self.profile}"


class UserConnection(models.Model):
    user_profile = models.ForeignKey(
        UserProfileSettings, related_name="user_connections", on_delete=models.CASCADE
    )
    other_profile = models.ForeignKey(UserProfileSettings, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        default=datetime.utcnow,
        help_text="The datetime this connection was created.",
    )
    connection_type = models.CharField(
        default="", max_length=256, help_text="Type of the connection (Friend, ...)"
    )
    connection_state = models.CharField(
        default="",
        max_length=256,
        help_text="State of the connection (Accepted, Request, ...)",
    )

    def __str__(self):
        return f"{self.user_profile}_{self.other_profile}"
