from django.urls import path
from .views import LoginView, RegisterView, ActivateView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("activate/",ActivateView.as_view(), name="activate"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
