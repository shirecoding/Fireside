__all__ = ["UserProfileSerializer"]

from user_profile.models import UserProfile, UserRelationship, GameMembership
from rest_framework import serializers


class GameMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMembership
        fields = ["game", "last_updated", "is_online"]


class UserRelationshipSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="other_profile")
    is_online = serializers.BooleanField(source="other_profile.is_online")
    games = GameMembershipSerializer(
        source="other_profile.memberships", many=True, read_only=True
    )

    class Meta:
        model = UserRelationship
        fields = [
            "user",
            "relationship_type",
            "relationship_state",
            "is_online",
            "games",
        ]


class UserProfileSerializer(serializers.ModelSerializer):

    relationships = UserRelationshipSerializer(
        source="user_relationships", many=True, read_only=True
    )
    games = GameMembershipSerializer(source="memberships", many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "title",
            "about",
            "settings",
            "relationships",
            "games",
            "color_theme",
        ]
