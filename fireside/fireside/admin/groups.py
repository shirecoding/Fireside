from django.contrib.auth.models import Group
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.models import Permission

from fireside.utils.forms import HorizontalFilterField
from toolz import dissoc
from itertools import chain

app_labels = sorted(
    Permission.objects.values_list("content_type__app_label", flat=True)
    .distinct()
    .order_by()
)


class PermissionsForm(ModelForm):
    """
    Creates a horizontal filter field form for each app in `Permissions`
    """

    class Meta:
        model = Group
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for app in app_labels:
            self.fields[app] = HorizontalFilterField(
                app,
                queryset=Permission.objects.filter(content_type__app_label=app),
                required=False,
            )
            self.initial[app] = self.instance.permissions.all()

    def _save_m2m(self):
        super()._save_m2m()
        self.instance.permissions.set(
            chain.from_iterable(
                v for k, v in self.cleaned_data.items() if k in app_labels
            )
        )
        self.instance.save()


class GroupAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    form = PermissionsForm
    fieldsets = [(None, {"fields": ["name"]})]
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(
            request,
            obj,
            **dissoc(
                kwargs, "fields"
            ),  # prevent looking up the fields itself by calling `self.get_fieldsets` modelform_factory complaining about non-existent fields
            fields=flatten_fieldsets(self.fieldsets)
        )

    def get_fieldsets(self, request, obj: Group = None):
        return [
            *super().get_fieldsets(request, obj),
            ["Application Permissions", {"fields": list(app_labels)}],
        ]


# replace default GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
