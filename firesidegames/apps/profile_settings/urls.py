from django.urls import path
from .views import index_view

app_name = "profile_settings"  # namespace for {% url 'profile_settings:index' %} etc..

urlpatterns = [
    path("", index_view, name="index"),
]
