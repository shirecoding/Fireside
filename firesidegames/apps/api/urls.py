from django.urls import path
from .views import UserList, UserDetail, UserProfileDetail

app_name = "api"

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<str:username>", UserDetail.as_view()),
    path("user_profiles/<str:username>", UserProfileDetail.as_view()),
]
