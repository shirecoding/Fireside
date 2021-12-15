from django.urls import path
from .views import UserList, UserDetail

app_name = "api"

urlpatterns = [
    path("users/", UserList.as_view(), name="users"),
    path("users/<int:pk>", UserDetail.as_view()),
]
