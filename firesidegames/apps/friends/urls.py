from django.urls import path
from .views import index_view

app_name = "friends"  # namespace for {% url 'friends:index' %} etc..

urlpatterns = [
    path("", index_view, name="index"),
]
