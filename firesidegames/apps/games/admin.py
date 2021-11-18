from django.contrib import admin
from .models import Game, Category, GameInstance


class GameInstanceInline(admin.TabularInline):
    """
    When creating a new instance from inline, a default random uid for the instance is created,
    slightly modify it so that django detects a change, else it will no create a new instance
    """

    model = GameInstance
    extra = 0


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Game", {"fields": ["name", "short_description", "long_description"]}),
        ("Properties", {"fields": ["categories", "image"]}),
    ]
    inlines = [
        GameInstanceInline,
    ]


admin.site.register(Game, GameAdmin)
admin.site.register(Category)
admin.site.register(GameInstance)
