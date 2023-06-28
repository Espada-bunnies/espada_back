import logging
from rest_framework.authentication import TokenAuthentication

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.models import User,UserProfile
from apps.users.serializers import (ActivateUserSerializer,
                                    ChangePasswordSerializer,
                                    LoginUserSerializer,
                                    RegisterUserSerializer,
                                    UserProfileSerializer)
from apps.users.services import ActivationService, LoginService

logger = logging.getLogger("django")


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginUserSerializer, responses=LoginUserSerializer, tags=["Auth"]
    )
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = LoginService.login_user(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    @extend_schema(
        request=RegisterUserSerializer, responses=RegisterUserSerializer, tags=["Auth"]
    )
    def post(self, request):
        serializer = RegisterUserSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class ActivateView(views.APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    @extend_schema(
        request=None, responses={200: {"description": "Success message"}}, tags=["Auth"]
    )
    def get(self, request, pk=None):
        logger.info(request.query_params)
        id = ActivationService.decode_uid(request.query_params.get("uid"))
        request.query_params._mutable = True
        request.query_params["id"] = id
        user = User.objects.filter(id=id).first()
        serializer = ActivateUserSerializer(data=request.query_params, instance=user)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message:": "Account verified successfully"}, status=status.HTTP_200_OK
        )


class ResendActivationView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @extend_schema(
        request=None, responses={200: {"description": "Success message"}}, tags=["Auth"]
    )
    def post(self, request):
        user = User.objects.filter(email=request.data.get("email")).first()
        if user:
            ActivationService.send_activation_email(user)
            return Response(
                {"message:": "Activation email sent successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message:": "User with this email does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: {"description": "Success message"}},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message:": "Password changed successfully"}, status=status.HTTP_200_OK
        )


class ResetPasswordView(views.APIView):
    """
    This view is used to send reset password link to user's email after registration or login
    """
    authentication_classes = [TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(OpenApiTypes.OBJECT)},
        tags=["Auth"],
    )
    def get(self, request):
        ActivationService.send_reset_password_link(request, request.user)




class UserProfileView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = User.objects.filter(username=request.user).first()
        profile = user.user_profile

        user_profile_serializer = UserProfileSerializer(profile)

        return Response(user_profile_serializer.data)


    def patch(self, request):
        profile = request.user.user_profile

        profile = UserProfileSerializer(profile,data=request.data,partial=True)

        if profile.is_valid(raise_exception=True):
            profile.save()
            return Response(profile.data)

        return Response(profile._errors)


