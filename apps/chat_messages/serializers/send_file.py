from rest_framework import serializers

from apps.chat_messages.constants import TEXT_CONTENT_MAX_LENGTH, MAX_FILES_PER_MESSAGE

class SendFileSerializer(serializers.Serializer):
    """Send file message request serializer"""
    file_ids = serializers.ListField(
        child = serializers.UUIDField(),
        allow_empty = False,
        max_length=MAX_FILES_PER_MESSAGE,
        error_messages={
            "max_length": f"A message can contain at most {MAX_FILES_PER_MESSAGE} files.",
        },
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