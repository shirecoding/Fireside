__all__ = ["ModelAdmin"]

from guardian.admin import GuardedModelAdmin
from fireside.models import Model


class ModelAdmin(GuardedModelAdmin):
    """
    - Adds object level permissions (groups, users) via django-guardian
    - Handle field level permissions (requires the model to be instance of fireside.Model)
    """

    def get_readonly_fields(
        self, request, obj: Model | None = None
    ) -> tuple[str] | list[str]:
        if obj:
            fields = super().get_readonly_fields(request, obj)
            if request.user.is_superuser:
                return fields
            else:
                return tuple(
                    f
                    for f in fields
                    if hasattr(obj, f)
                    and (
                        obj.has_field_perm(request.user, "view", getattr(obj, f))
                        or obj.has_field_perm(request.user, "change", getattr(obj, f))
                    )
                )

        return self.readonly_fields
