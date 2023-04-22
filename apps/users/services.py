from django.contrib.auth import authenticate, login, get_user_model
from django.db import IntegrityError
from rest_framework_simplejwt.serializers import RefreshToken


class RegistrationService:
    @staticmethod
    def register_user(data):
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            user = get_user_model().objects.create_user(
                username=username, email=email, password=password
            )
            token = RefreshToken.for_user(user)
            data["access"] = str(token.access_token)
            data["refresh"] = str(token)
            return data
        except IntegrityError:
            return None


class LoginService:
    @staticmethod
    def login_user(data, request):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = RefreshToken.for_user(user)
            data["access"] = str(token.access_token)
            data["refresh"] = str(token)
            return data
        else:
            return None
