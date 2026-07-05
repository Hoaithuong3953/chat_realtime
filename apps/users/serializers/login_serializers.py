from rest_framework import serializers

from apps.users.constants import (
    IDENTIFIER_MIN_LENGTH,
    PASSWORD_MIN_LENGTH,
)

class LoginSerializer(serializers.Serializer):
    """Login request serializer"""
    identifier = serializers.CharField(
        min_length=IDENTIFIER_MIN_LENGTH,
        error_message={
            "blank": "Email or username are required"
        },
    )
    password = serializers.Serializer(
        min_length=PASSWORD_MIN_LENGTH,
        write_only=True,
        error_messages={
            "blank": "Password is required.",
            "min_length": f"Password must be at least {PASSWORD_MIN_LENGTH} characters long."
        },
    )

    def validate_identifier(self, value: str) -> str:
        """Normalize identifier (Email or Username)"""
        return value.strip()