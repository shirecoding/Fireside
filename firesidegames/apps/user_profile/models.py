from django.db import models
import django.contrib.auth
from games.models import Game
from django.utils import timezone
from user_profile.utils import Constants
from django.contrib.sessions.models import Session
from datetime import timedelta


class UserProfile(models.Model):
    """
    Notes:
        - Created during user registration (see signals/handlers.py)
    """

    user = models.OneToOneField(
        django.contrib.auth.get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    last_updated = models.DateTimeField(
        default=timezone.now, help_text="The last datetime of any user activity."
    )

    about = models.TextField(max_length=4096, default="", blank=True)
    title = models.CharField(max_length=256, default=Constants.UserTitles.initiate)
    settings = models.JSONField(
        default=dict, help_text="User profile in JSON or YAML format.", blank=True
    )
    games = models.ManyToManyField(Game, through="GameMembership")
    relationships = models.ManyToManyField("self", through="UserRelationship")
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
        return f"{self.user.username}"

    @property
    def is_online(self):
        return timezone.now() - self.last_updated < timedelta(minutes=15)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)


class GameMembership(models.Model):
    profile = models.ForeignKey(
        UserProfile, related_name="game_memberships", on_delete=models.CASCADE
    )
    game = models.ForeignKey(Game, related_name="memberships", on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime the user created an account for the game.",
    )
    last_updated = models.DateTimeField(
        default=timezone.now, help_text="The last datetime the user played the game."
    )

    def __str__(self):
        return f"{self.game}_{self.profile}"

    @property
    def is_online(self):
        return timezone.now() - self.last_updated < timedelta(minutes=15)


class UserRelationship(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, related_name="user_relationships", on_delete=models.CASCADE
    )
    other_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime this connection was created.",
    )
    relationship_type = models.CharField(
        default=Constants.UserRelationshipType.friend,
        choices=(
            (v, v)
            for k, v in Constants.UserRelationshipType.__dict__.items()
            if not k.startswith("__")
        ),
        max_length=256,
        help_text="Type of the connection (Friend, ...)",
    )
    relationship_state = models.CharField(
        default=Constants.UserRelationshipState.request,
        choices=(
            (v, v)
            for k, v in Constants.UserRelationshipState.__dict__.items()
            if not k.startswith("__")
        ),
        max_length=256,
        help_text="State of the connection (Accepted, Request, ...)",
    )

    def __str__(self):
        return f"{self.user_profile}_{self.other_profile}"


class Mail(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
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
