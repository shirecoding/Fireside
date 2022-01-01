from django.db import models
import django.contrib.auth
from games.models import Game
from django.utils import timezone
from user_profile.utils import Constants
from django.contrib.sessions.models import Session
from datetime import timedelta
from user_profile.utils import Constants as UserProfileConstants
import logging

logger = logging.getLogger(__name__)


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
    relationships = models.ManyToManyField(
        "self",
        through="UserRelationship",
        through_fields=("user_profile", "other_profile"),
    )
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

    def request_user_relationship(self, other_profile, relationship_type):
        if (
            not UserRelationship.objects.filter(
                user_profile=self,
                other_profile=other_profile,
                relationship_type=relationship_type,
            ).exists()
            and self != other_profile
        ):
            UserRelationship.objects.create(
                user_profile=self,
                other_profile=other_profile,
                relationship_type=relationship_type,
                relationship_state=UserProfileConstants.UserRelationshipState.request,
            )

    def accept_user_relationship(self, other_profile, relationship_type):
        if self != other_profile:
            UserRelationship.objects.update_or_create(
                user_profile=self,
                other_profile=other_profile,
                defaults={
                    "relationship_type": relationship_type,
                    "relationship_state": UserProfileConstants.UserRelationshipState.accepted,
                },
            )

    def reject_user_relationship(self, other_profile, relationship_type):
        qs = UserRelationship.objects.filter(
            user_profile=self,
            other_profile=other_profile,
            relationship_type=relationship_type,
        )
        if qs.exists():
            qs.first().delete()

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
        UserProfile,
        related_name="user_relationships",
        on_delete=models.CASCADE,
        blank=False,
    )
    other_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=False
    )
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

    class Meta:
        unique_together = ("user_profile", "other_profile", "relationship_type")

    def __str__(self):
        return f"{self.user_profile}_{self.other_profile}"

    def is_synced(self, obj):
        return obj.relationship_state == self.relationship_state

    def sync_profile(self, other_profile, relationship_type):
        """
        Synchronize other_profile with this profile
        """

        qs = UserRelationship.objects.filter(
            user_profile=other_profile, relationship_type=relationship_type
        )
        instance = qs.first() if qs.exists() else None
        if instance and not self.is_synced(instance):
            instance.relationship_state = self.relationship_state
            instance.save()

    def save(self, *args, **kwargs):

        # create
        if self._state.adding:
            super().save(*args, **kwargs)

            # create symmetrical relationship
            UserRelationship.objects.update_or_create(
                user_profile=self.other_profile,
                other_profile=self.user_profile,
                relationship_type=self.relationship_type,
                defaults={
                    "relationship_state": self.relationship_state,
                },
            )

        # update
        else:
            super().save(*args, **kwargs)
            self.sync_profile(self.other_profile, self.relationship_type)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        qs = UserRelationship.objects.filter(
            user_profile=self.other_profile,
            other_profile=self.user_profile,
            relationship_type=self.relationship_type,
        )
        if qs.exists():
            qs.first().delete()


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
