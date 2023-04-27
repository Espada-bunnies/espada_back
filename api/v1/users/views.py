from rest_framework import views, status, viewsets, permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from apps.users.tokens import activation_token
from apps.users.serializers import LoginUserSerializer, RegisterUserSerializer, ActivateUserSerializer, ChangePasswordSerializer
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
    
    
class ActivateView(views.APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    
    def post(self, request, pk=None):
        # TODO: Try to remove id(getting id from token)
        user = User.objects.filter(id=request.data.get("id")).first()
        if user is None:
            return Response({"message:": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ActivateUserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message:": "Account activated successfully"}, status=status.HTTP_200_OK)
    

class ChangePasswordView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message:": "Password changed successfully"}, status=status.HTTP_200_OK)