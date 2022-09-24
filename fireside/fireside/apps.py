from django.apps import AppConfig


class FiresideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fireside"

    def ready(self):
        pass
