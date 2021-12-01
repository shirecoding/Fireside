from profile_settings.models import UserProfileSettings, Mail
from django.contrib import admin
from django.db.models import JSONField
from firesidegames.utils import YAMLWidget


class GameMembershipInline(admin.TabularInline):
    model = UserProfileSettings.games.through
    extra = 0


class UserConnectionsInline(admin.TabularInline):
    model = UserProfileSettings.connections.through
    fk_name = "other_profile"
    extra = 0


class MailInline(admin.TabularInline):
    model = Mail
    extra = 0


class UserProfileSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": YAMLWidget}}
    inlines = [GameMembershipInline, UserConnectionsInline, MailInline]
    exclude = ("games", "connections", "mail")


admin.site.register(UserProfileSettings, UserProfileSettingsAdmin)
