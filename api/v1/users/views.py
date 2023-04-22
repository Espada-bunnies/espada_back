from rest_framework import views, status, viewsets, permissions
from rest_framework.response import Response
from apps.users.serializers import LoginUserSerializer, RegisterUserSerializer
from apps.users.models import User


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
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
