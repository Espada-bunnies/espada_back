from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError, EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginValidator:
    def __init__(self, data):
        self.data = data
        self.is_valid = False
        self.errors = {}

    def validate_username(self):
        errors = self.errors
        username = self.data.get("username")
        if not User.objects.filter(username=username).exists():
            errors["username"] = _("User does not exist")

    def validate_password(self):
        password = self.data.get("password")
        errors = self.errors

        if not User.objects.filter(password=password).exists():
            errors["password"] = _("Password is incorrect")

    def validate(self):
        self.validate_username()
        self.validate_password()
        if not self.errors:
            self.is_valid = True
        return self.data


class RegistrationValidator(LoginValidator):
    def __init__(self, data):
        super().__init__(data)

    def validate_username(self):
        errors = self.errors
        errors["username"] = []
        username = self.data.get("username")
        if User.objects.filter(username=username).exists():
            errors["username"].append(_("Username already exists"))
        if len(username) < 6:
            errors["username"].append(_("Username must be at least 6 characters long"))
        if not username.isalnum():
            errors["username"].append(_("Username must be alphanumeric"))
        if len(errors["username"]) == 0:
            del errors["username"]

    def validate_password(self):
        errors = self.errors
        errors["password"] = []
        password = self.data.get("password")
        if len(password) < 8:
            errors["password"].append(_("Password must be at least 8 characters long"))
        if password.isalnum():
            errors["password"].append(
                _("Password must contain at least one special character")
            )

    def validate_confirm_password(self):
        errors = self.errors
        password = self.data.get("password")
        confirm_password = self.data.get("confirm_password")
        if password != confirm_password:
            errors["password"].append(_("Passwords do not match"))
        if len(errors["password"]) == 0:
            del errors["password"]

    def validate_email(self):
        email = self.data.get("email")
        errors = self.errors
        errors["email"] = []
        if not email:
            errors["email"].append(_("Email is required"))
        if User.objects.filter(email=email).exists():
            errors["email"].append(_("Email already exists"))
        if len(errors["email"]) == 0:
            del errors["email"]

    def validate(self):
        self.validate_username()
        self.validate_password()
        self.validate_confirm_password()
        self.validate_email()
        if not self.errors:
            self.is_valid = True
        return self.data
