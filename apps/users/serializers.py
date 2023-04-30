from rest_framework import serializers
from django.core.exceptions import ValidationError
from .services import RegistrationService, LoginService, ActivationService
from .validators import (
    RegisterValidator,
    LoginValidator,
    ActivationTokenValidator,
    ResetPasswordValidator,
)
from django.db.transaction import atomic


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
        validator = RegisterValidator(attrs)
        return validator.validate()

    @atomic
    def create(self, validated_data):
        data, user = RegistrationService.register_user(data=validated_data)
        if data is not None:
            ActivationService.send_activate_link(
                request=self.context.get("request"), user=user
            )
            return user
        raise ValidationError("Error occurred while creating user")


class ActivateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        return ActivationTokenValidator(attrs).validate()

    def update(self, instance, validated_data):
        return ActivationService.activate_user(instance)


# TODO: Refactor this
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context.get("user")
        validator = ResetPasswordValidator(attrs)
        return validator.validate()

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
