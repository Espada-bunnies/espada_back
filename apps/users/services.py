from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.db import IntegrityError
from .tokens import activation_token
from rest_framework_simplejwt.serializers import RefreshToken
from django.db.transaction import atomic

class RegistrationService:
    @staticmethod
    @atomic
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
            send_activate_link(user)
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
        
        
        
def send_activate_link(user):
    send_mail(
        subject="Activate your account",
        message=f"{activation_token.make_token(user)} {user.id}",
        from_email="espada@noreply.org",
        recipient_list=[user.email],
    )