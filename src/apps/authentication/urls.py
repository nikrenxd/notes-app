from dj_rest_auth import views
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path

urlpatterns = [
    path("auth/login", views.LoginView.as_view(), name="login"),
    path("auth/refresh", get_refresh_view().as_view(), name="token_refresh"),
    path("auth/logout", views.LogoutView.as_view(), name="logout"),
]
