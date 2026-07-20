from rest_framework import serializers

from apps.chats.constants import TITLE_MAX_LENGTH

class CreateGroupChatSerializer(serializers.Serializer):
    """Create group chat request serializer"""
    title = serializers.CharField(
        max_length=TITLE_MAX_LENGTH,
        required=True,
        allow_blank=False,
        error_messages={
            "max_length": f"The title must be not exceed {TITLE_MAX_LENGTH} characters long.",
        }
    )
    member_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
    )

    def validate_member_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate members are not allowed.",
            )
        return value