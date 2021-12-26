from django.urls import path
from .views import UserProfileDetail, AuthenticateUser

app_name = "api"

urlpatterns = [
    path("user/", UserProfileDetail.as_view()),  # own user profile
    path(
        "auth/user/", AuthenticateUser.as_view()
    ),  # authenticate user from 3rd party clients
]
