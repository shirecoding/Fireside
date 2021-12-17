from django.urls import path
from .views import UserProfileDetail

app_name = "api"

urlpatterns = [
    path("user/", UserProfileDetail.as_view()),  # own user profile
]
