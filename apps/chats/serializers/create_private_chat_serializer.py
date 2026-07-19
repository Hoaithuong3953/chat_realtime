from rest_framework import serializers

class CreatePrivateChatSerializer(serializers.Serializer):
    """Private chat request serializer"""
    target_user_id = serializers.UUIDField(
        error_messages={
            "invalid": "Invalid target user."
        }
    )