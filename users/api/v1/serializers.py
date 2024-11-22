from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordChangeSerializer, PasswordResetSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.forms import AllAuthPasswordResetForm
from users.models import User


class PasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = AllAuthPasswordResetForm


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField(region="PH")
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user: User):
        user.phone_number = self.validated_data.get("phone_number")
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.save(update_fields=["phone_number", "first_name", "last_name"])

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Unable to register with the provided email address."
            )

        return value


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    def custom_validation(self, attrs):
        if len(attrs.get("new_password1")) < 8:
            raise serializers.ValidationError(
                {"new_password1": "Must be at least 8 characters."}
            )

        if attrs.get("new_password1") == attrs.get("old_password"):
            raise serializers.ValidationError(
                {
                    "new_password1": "New password cannot be the same as current password."
                }
            )

        if attrs.get("new_password1") != attrs.get("new_password2"):
            raise serializers.ValidationError(
                {"new_password2": "Passwords do not match."}
            )

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError("Incorrect password. Try again.")
        return value
