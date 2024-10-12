from django.urls import path

from src.apps.users.views import UserCreateView


urlpatterns = [
    path("auth/register/", UserCreateView.as_view(), name="user-create"),
]
