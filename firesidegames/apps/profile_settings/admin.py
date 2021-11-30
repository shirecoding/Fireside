from profile_settings.models import UserProfileSettings
from django.contrib import admin
from django.db.models import JSONField
from firesidegames.utils import YAMLWidget


class GameMembershipInline(admin.TabularInline):
    model = UserProfileSettings.games.through
    extra = 0


class UserProfileSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": YAMLWidget}}
    inlines = [
        GameMembershipInline,
    ]
    exclude = ("games",)


admin.site.register(UserProfileSettings, UserProfileSettingsAdmin)
