from rest_framework import serializers

class TransferOwnershipSerializer(serializers.Serializer):
    """Transfer group ownership to another member request serializer"""
    new_owner_id = serializers.UUIDField(
        required=True,
    )