from rest_framework import serializers

class CreateAIRequestSerializer(serializers.Serializer):
    """Create a request to the AI service request serializer"""
    message_id = serializers.UUIDField(
        required=True,
    )