from rest_framework import serializers

class UpdateAccountSerializer(serializers.Serializer):
    """Serializer for updating account status"""
    is_active = serializers.BooleanField(required=True)