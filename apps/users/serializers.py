from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User
from .services import RegistrationService, LoginService
from .validators import RegistrationValidator, LoginValidator, validate_activation_token


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
        user = RegistrationService.register_user(data=validated_data)
        if user is not None:
            return user
        raise ValidationError("Error occurred while creating user")


class ActivateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    token = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        return validate_activation_token(attrs)
    
    def update(self, instance, validated_data):
        instance.is_active = True
        instance.is_verified = True
        instance.save()
        return instance
    

# TODO: Refactor this
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        user = self.context.get("user")
        validator = RegistrationValidator(attrs)
        validator.validate_password()
        if validator.errors:
            raise ValidationError(validator.errors)
        if user.check_password(attrs.get("old_password")):
            return attrs
        raise ValidationError({"old_password": "Old password is incorrect"})
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance