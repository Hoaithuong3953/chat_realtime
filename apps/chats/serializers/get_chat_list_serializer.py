from rest_framework import serializers

from apps.chats.constants import (
    LIMIT_CHAT_DEFAULT_VALUE,
    LIMIT_CHAT_MAX_VALUE,
    LIMIT_CHAT_MIN_VALUE,
)

class GetChatListSerializer(serializers.Serializer):
    """Get chat list request serializer"""
    before = serializers.CharField(
        required=False,
    )
    limit = serializers.IntegerField(
        required=False,
        default=LIMIT_CHAT_DEFAULT_VALUE,
        min_value=LIMIT_CHAT_MIN_VALUE,
        max_value=LIMIT_CHAT_MAX_VALUE,
        error_messages={
            "min_value": f"The limit chat must be greater than or equal to {LIMIT_CHAT_MIN_VALUE}.",
            "max_value": f"The limit chat must not exceed {LIMIT_CHAT_MAX_VALUE}.",
        }
    )