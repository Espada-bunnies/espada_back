from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.db import IntegrityError
from .tokens import activation_token
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
            data["access_token"] = str(token.access_token)
            data["refresh_token"] = str(token)
            return data, user
        except IntegrityError:
            return None


class LoginService:
    @staticmethod
    def login_user(request, data):
        username = data.get("username")
        password = data.pop("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user=user)
            try:
                token = RefreshToken.objects.get(user=user)
            except RefreshToken.DoesNotExist:
                token = RefreshToken.for_user(user)
            data["access"] = str(token.access_token)
            data["refresh"] = str(token)
            return data
        else:
            return None


class ActivationService:
    @staticmethod
    def activate_user(user):
        if user is not None:
            user.is_active = True
            user.is_verified = True
            user.save()
            return user
        else:
            return None

    @staticmethod
    def decode_uid(uidb64):
        return urlsafe_base64_decode(uidb64).decode()

    @staticmethod
    def send_activate_link(request, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        send_mail(
            subject="Verify your email",
            message=request.build_absolute_uri(
                f"{reverse('activate')}?token={activation_token.make_token(user)}&uid={uidb64}"
            ),
            from_email="espada@noreply.org",
            recipient_list=[user.email],
        )
