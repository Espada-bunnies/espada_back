from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User
from .services import RegistrationService, LoginService
from .validators import RegistrationValidator, LoginValidator


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validator = LoginValidator(attrs)
        validator.validate()
        if validator.is_valid:
            return LoginService.login_user(data=attrs)
        raise ValidationError(validator.errors)


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validator = RegistrationValidator(attrs)
        validator.validate()
        if validator.is_valid:
            return attrs
        raise ValidationError(validator.errors)

    def create(self, validated_data):
        return RegistrationService.register_user(data=validated_data)
