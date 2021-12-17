from django.contrib import admin
from .models import Game, Category, GameInstance
from django.forms.models import ModelForm


class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """Should returns True if data differs from initial.
        By always returning true even unchanged inlines will get validated and saved."""
        return True


class GameInstanceInline(admin.TabularInline):
    """
    When creating a new instance from inline, a default random uid for the instance is created,
    slightly modify it so that django detects a change, else it will no create a new instance
    """

    model = GameInstance
    extra = 0
    form = AlwaysChangedModelForm


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
