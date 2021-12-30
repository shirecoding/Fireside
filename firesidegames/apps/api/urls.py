from django.urls import path
from .views import UserProfileDetail, AuthenticateUser, friend_request

app_name = "api"

urlpatterns = [
    # user
    path("user/", UserProfileDetail.as_view(), name="user_detail"),
    path("user/friend_request", friend_request, name="friend_request"),
    # auth
    path(
        "auth/user/", AuthenticateUser.as_view(), name="auth_user"
    ),  # authenticate user from 3rd party clients
]
