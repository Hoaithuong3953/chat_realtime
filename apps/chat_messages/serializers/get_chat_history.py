from rest_framework import serializers

from apps.chat_messages.constants import (
    LIMIT_MESSAGE_DEFAULT_VALUE,
    LIMIT_MESSAGE_MAX_VALUE,
    LIMIT_MESSAGE_MIN_VALUE,
)

class GetChatHistorySerializer(serializers.Serializer):
    """Get chat history request serializer"""
    before = serializers.CharField(
        required=False,
    )
    limit = serializers.IntegerField(
        required=False,
        default=LIMIT_MESSAGE_DEFAULT_VALUE,
        min_value=LIMIT_MESSAGE_MIN_VALUE,
        max_value=LIMIT_MESSAGE_MAX_VALUE,
        error_messages={
            "min_value": f"The limit message must be greater than or equal to {LIMIT_MESSAGE_MIN_VALUE}.",
            "max_value": f"The limit message must not exceed {LIMIT_MESSAGE_MAX_VALUE}.",
        }
    )