from rest_framework import serializers

from apps.users.dto import RegisterRequest

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration request
    """
    email = serializers.EmailField(
        error_messages={
            "blank": "Email is required.",
            "invalid": "Email format is invalid.",
        }
    )
    username = serializers.CharField(
        error_messages={
            "blank": "Username is required.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": "Password is required.",
        },
    )
    name = serializers.CharField(
        error_messages={
            "blank": "Name is required.",
        },
    )

    def validate_email(self, value: str) -> str:
        """Normalize the email address"""
        return value.strip().lower()

    def validate_username(self, value: str) -> str:
        """Normalize the username"""
        return value.strip()

    def to_dto(self) -> RegisterRequest:
        """Convert validated serializer data to application DTO"""
        return RegisterRequest.model_validate(self.validated_data)