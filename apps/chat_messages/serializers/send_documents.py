from rest_framework import serializers

from apps.chat_messages.constants import TEXT_CONTENT_MAX_LENGTH

class SendDocumentSerializer(serializers.Serializer):
    """Send document message request serializer"""
    chat_id = serializers.UUIDField(
        required=True,
    )
    file_ids = serializers.ListField(
        child = serializers.UUIDField(),
        allow_empty = False,
    )
    text_content = serializers.CharField(
        required=False,
        max_length=TEXT_CONTENT_MAX_LENGTH,
        error_messages={
            "max_length": f"The text content must be not exceed {TEXT_CONTENT_MAX_LENGTH} characters long.",
        }
    )
    reply_to_message = serializers.UUIDField(
        required=False,
        allow_null=True,
    )