from django.urls import path
from .views import index_view

app_name = "user_profile"  # namespace for {% url 'user_profile:index' %} etc..

urlpatterns = [
    path("", index_view, name="index"),
]
