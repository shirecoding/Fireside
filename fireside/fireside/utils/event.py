__all__ = ["register_event"]


from fireside.models import Event


def register_event(name: str, description: str = "") -> Event:
    return Event.objects.update_or_create(
        name=name,
        defaults={
            "description": description,
        },
    )[0]
