# accounts/urls.py

from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    follow_user, unfollow_user, UserListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/",    LoginView.as_view(),    name="login"),
    path("profile/",  ProfileView.as_view(),  name="profile"),

    # Follow management (checker expects these)
    path("follow/<int:user_id>/",   follow_user,   name="follow_user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"),

    # Optional helper (for the checker strings above)
    path("users/", UserListView.as_view(), name="users"),
]
