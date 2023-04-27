from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .tokens import activation_token

User = get_user_model()

class Validator:
    def __init__(self, data):
        self.data = data
        self.errors = {}

    def validate(self):
        raise NotImplementedError

    def validate_field_length(self, field_name, min_length):
        field_value = self.data.get(field_name)
        if field_value and len(field_value) < min_length:
            self.errors[field_name] = _(f"{field_name.capitalize()} must be at least {min_length} characters long")

    def validate_alphanumeric(self, field_name):
        field_value = self.data.get(field_name)
        if field_value and not field_value.isalnum():
            self.errors[field_name] = _(f"{field_name.capitalize()} must be alphanumeric")

    def validate_special_char(self, field_name):
        field_value = self.data.get(field_name)
        if field_value and field_value.isalnum():
            self.errors[field_name] = _(f"{field_name.capitalize()} must contain at least one special character")

class LoginValidator(Validator):
    def validate(self):
        username = self.data.get("username")
        password = self.data.get("password")

        user = User.objects.filter(username=username).first()
        if not user:
            self.errors["username"] = _("User does not exist")
        elif not user.check_password(password):
            self.errors["password"] = _("Password is incorrect")

        if self.errors:
            raise ValidationError(self.errors)

class RegistrationValidator(Validator):
    def validate(self):
        self.validate_field_length("username", 6)
        self.validate_alphanumeric("username")

        if User.objects.filter(username=self.data.get("username")).exists():
            self.errors["username"] = [_("Username already exists")]

        self.validate_field_length("password", 8)
        self.validate_special_char("password")

        if self.data.get("password") != self.data.get("confirm_password"):
            self.errors["password"] = [_("Passwords do not match")]

        email = self.data.get("email")
        if not email:
            self.errors["email"] = [_("Email is required")]
        elif User.objects.filter(email=email).exists():
            self.errors["email"] = [_("Email already exists")]

        if self.errors:
            raise ValidationError(self.errors)

def validate_activation_token(data):
    errors = {}
    user_id = data.get("id")
    token = data.get("token")
    if not user_id:
        errors["id"] = _("User id is required")
    if not token:
        errors["token"] = _("Token is required")

    user = User.objects.filter(id=user_id).first()
    if not user:
        errors["id"] = _("User does not exist")
    elif not activation_token.check_token(user=user, token=token):
        errors["token"] = _("Invalid token")

    if errors:
        raise ValidationError(errors)

    return data