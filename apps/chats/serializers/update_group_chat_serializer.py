from rest_framework import serializers

from apps.chats.constants import TITLE_MAX_LENGTH, AVATAR_URL_MAX_LENGTH

class UpdateGroupChatSerializer(serializers.Serializer):
    """Update group chat request serializer"""
    title = serializers.CharField(
        max_length=TITLE_MAX_LENGTH,
        required=True,
        allow_blank=False,
        error_messages={
            "max_length": f"The title must be not exceed {TITLE_MAX_LENGTH} characters long.",
        }
    )
    avatar_url = serializers.URLField(
        required=False,
        allow_null=True,
        max_length=AVATAR_URL_MAX_LENGTH,
        error_messages={
            "max_length": f"Avatar URL must not exceed {AVATAR_URL_MAX_LENGTH} characters long.",
        },
    )