from django.urls import path
from .views import UserProfileDetail, AuthenticateUser, friend_request

app_name = "api"

urlpatterns = [
    # user
    path("user/", UserProfileDetail.as_view()),
    path("user/friend_request", friend_request),
    # auth
    path(
        "auth/user/", AuthenticateUser.as_view()
    ),  # authenticate user from 3rd party clients
]
