from rest_framework import serializers
from apps.users.constants import (
    PAGE_DEFAULT,
    PAGE_MIN_VALUE,
    PAGE_SIZE_DEFAULT,
    PAGE_SIZE_MAX_VALUE,
    PAGE_SIZE_MIN_VALUE,
    KEYWORD_MAX_LENGTH,
)

class GetUsersSerializer(serializers.Serializer):
    """Get active user list request serializer"""
    q = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=KEYWORD_MAX_LENGTH,
        error_messages={
            "max_length": f"The search key must be not exceed {KEYWORD_MAX_LENGTH} characters long.",
        }
    )
    page = serializers.IntegerField(
        required=False,
        default=PAGE_DEFAULT,
        min_value=PAGE_MIN_VALUE,
        error_messages={
            "min_value": f"The number of pages must be greater than or equal to {PAGE_MIN_VALUE}.",
        }
    )
    page_size = serializers.IntegerField(
        required=False,
        default=PAGE_SIZE_DEFAULT,
        min_value=PAGE_SIZE_MIN_VALUE,
        max_value=PAGE_SIZE_MAX_VALUE,
        error_messages={
            "min_value": f"The page size must be greater than or equal to {PAGE_SIZE_MIN_VALUE}.",
            "max_value": f"The page size must not exceed {PAGE_SIZE_MAX_VALUE}.",
        }
    )