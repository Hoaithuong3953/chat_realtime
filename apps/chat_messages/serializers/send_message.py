from rest_framework import serializers

class SendMessageSerializer(serializers.Serializer):
    """Add a message to chat request serializer"""
    text_content = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    reply_to_message = serializers.UUIDField(
        required=False,
        allow_null=True
    )