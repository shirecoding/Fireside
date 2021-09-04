# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # Includes the following:
    #
    #   accounts/login/ [name='login']
    #   accounts/logout/ [name='logout']
    #   accounts/password_change/ [name='password_change']
    #   accounts/password_change/done/ [name='password_change_done']
    #   accounts/password_reset/ [name='password_reset']
    #   accounts/password_reset/done/ [name='password_reset_done']
    #   accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #   accounts/reset/done/ [name='password_reset_complete']
]
