from django.urls import path

from src.apps.users.views import UserCreateView


urlpattern = [
    path("/auth/register", UserCreateView.as_view(), name="user-create"),
]
