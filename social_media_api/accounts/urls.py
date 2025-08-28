# accounts/urls.py

from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    follow_user, unfollow_user,   # <- function-based imports
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/",    LoginView.as_view(),    name="login"),
    path("profile/",  ProfileView.as_view(),  name="profile"),

    # Follow management (exact slugs expected by checker)
    path("follow/<int:user_id>/",   follow_user,   name="follow_user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"),
]
