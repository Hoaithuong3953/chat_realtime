import re
from rest_framework import serializers

from apps.accounts.constants import (
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    PASSWORD_MIN_LENGTH,
    FULL_NAME_MIN_LENGTH,
    FULL_NAME_MAX_LENGTH,
    USERNAME_PATTERN,
    PASSWORD_UPPERCASE_PATTERN,
    PASSWORD_LOWERCASE_PATTERN,
    PASSWORD_DIGIT_PATTERN,
    PASSWORD_SPECIAL_PATTERN,
)

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration request
    """
    email = serializers.EmailField(
        error_messages={
            "blank": "Email is required.",
            "invalid": "Email format is invalid.",
        },
    )

    username = serializers.RegexField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        regex=USERNAME_PATTERN,
        error_messages={
            "blank": "Username is required.",
            "min_length": f"Username must be at least {USERNAME_MIN_LENGTH} characters.",
            "max_length": f"Username must not exceed {USERNAME_MAX_LENGTH} characters.",
            "invalid": "Username must start with a letter and contain only letters, numbers, '.', '_' or '-'."
        },
    )

    password = serializers.CharField(
        write_only=True,
        min_length=PASSWORD_MIN_LENGTH,
        error_messages={
            "blank": "Password is required.",
            "min_length": f"Password must be at least {PASSWORD_MIN_LENGTH} characters long.",
        }
    )

    full_name = serializers.CharField(
        min_length=FULL_NAME_MIN_LENGTH,
        max_length=FULL_NAME_MAX_LENGTH,
        error_messages={
            "blank": "Full name is required.",
            "min_length": f"Fullname must be at least {FULL_NAME_MIN_LENGTH} characters long.",
            "max_length": f"Fullname must not exceed {FULL_NAME_MAX_LENGTH} characters long.",
        },
    )

    def validate_email(self, value: str) -> str:
        """Normalize and validation email"""
        return value.strip().lower()
        
    def validate_username(self, value: str) -> str:
        """Normalize and validation username"""
        return value.strip().lower()
    
    def validate_password(self, value: str) -> str:
        """Validation password strength"""
        if not re.search(PASSWORD_UPPERCASE_PATTERN, value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        
        if not re.search(PASSWORD_LOWERCASE_PATTERN, value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(PASSWORD_DIGIT_PATTERN, value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search(PASSWORD_SPECIAL_PATTERN, value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value