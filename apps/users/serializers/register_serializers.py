from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(
        error_messages={
            "blank": "Email is required.",
            "invalid": "Email format is invalid.",
        }
    )
    username = serializers.CharField(
        min_length=3,
        max_length=50,
        error_messages={
            "blank": "Username is required.",
            "min_length": "Username must be at least 3 characters.",
            "max_length": "Username is too long.",
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "blank": "Password is required.",
            "min_length": "Password must be at least 8 characters.",
        }
    )
    name = serializers.CharField(
        min_length=2,
        error_messages={
            "blank": "Name is required.",
            "min_length": "Name must be at least 2 characters long."
        }
    )

    def validate_email(self, value: str) -> str:
        """Normalize email"""
        return value.strip().lower()

    def validate_username(self, value: str) -> str:
        """Validate and normalize username"""
        return value.strip()