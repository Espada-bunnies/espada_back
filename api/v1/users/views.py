from rest_framework import views, status, viewsets, permissions
from rest_framework.response import Response
from apps.users.serializers import (
    LoginUserSerializer,
    RegisterUserSerializer,
    ActivateUserSerializer,
    ChangePasswordSerializer,
)
from apps.users.models import User
from apps.users.services import ActivationService
import logging

logger = logging.getLogger("django")


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = RegisterUserSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateView(views.APIView):
    # TODO: Add get method to send activation link again
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, pk=None):
        logger.info(request.query_params)
        id = ActivationService.decode_uid(request.query_params.get("uid"))
        request.query_params._mutable = True
        request.query_params["id"] = id
        user = User.objects.filter(id=id).first()
        serializer = ActivateUserSerializer(data=request.query_params, instance=user)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message:": "Account activated successfully"}, status=status.HTTP_200_OK
        )


class ChangePasswordView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message:": "Password changed successfully"}, status=status.HTTP_200_OK
        )
