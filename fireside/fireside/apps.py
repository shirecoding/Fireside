from django.apps import AppConfig


class FiresideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fireside"

    def ready(self):
        import fireside.tasks  # noqa
        from fireside.events import start_listening  # noqa

        # start listening for events
        start_listening()
