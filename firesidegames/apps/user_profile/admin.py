from user_profile.models import UserProfile, Mail
from django.contrib import admin
from django.db.models import JSONField
from firesidegames.utils import YAMLWidget


class GameMembershipInline(admin.TabularInline):
    model = UserProfile.games.through
    extra = 0


class UserRelationshipsInline(admin.TabularInline):
    model = UserProfile.relationships.through
    fk_name = "other_profile"
    extra = 0


class MailInline(admin.TabularInline):
    model = Mail
    extra = 0


class UserProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": YAMLWidget}}
    inlines = [GameMembershipInline, UserRelationshipsInline, MailInline]
    exclude = ("games", "relationships", "mail")
    readonly_fields = ("session",)


admin.site.register(UserProfile, UserProfileAdmin)
