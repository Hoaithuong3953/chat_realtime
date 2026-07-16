from rest_framework import serializers

from apps.users.constants import (
    FULL_NAME_MAX_LENGTH,
    FULL_NAME_MIN_LENGTH,
    AVATAR_URL_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    BIO_MAX_LENGTH,
    PHONE_NUMBER_PATTERN,
)

class UpdateProfileSerializer(serializers.Serializer):
    """Update profile request serializer"""
    full_name = serializers.CharField(
        required=False,
        min_length=FULL_NAME_MIN_LENGTH,
        max_length=FULL_NAME_MAX_LENGTH,
        error_messages={
            "min_length": f"Fullname must be at least {FULL_NAME_MIN_LENGTH} characters long.",
            "max_length": f"Fullname must not exceed {FULL_NAME_MAX_LENGTH} characters long.",
        },
    )

    avatar_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=AVATAR_URL_MAX_LENGTH,
        error_messages={
            "invalid": "Avatar URL must be a valid URL.",
            "max_length": f"Avatar URL must not exceed {AVATAR_URL_MAX_LENGTH} characters long.",
        },
    )

    phone_number = serializers.RegexField(
        regex=PHONE_NUMBER_PATTERN,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            "invalid": "Phone number is invalid."
        }
    )

    address = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=ADDRESS_MAX_LENGTH,
        error_messages={
            "max_length": f"Address must not exceed {ADDRESS_MAX_LENGTH} characters long.",
        },
    )

    dob = serializers.DateField(
        required=False,
        allow_null=True,
    )

    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=BIO_MAX_LENGTH,
        error_messages={
            "max_length": f"Bio must not exceed {BIO_MAX_LENGTH} characters long.",
        },
    )