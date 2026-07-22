from rest_framework import serializers

class AddMemberSerializer(serializers.Serializer):
    """Add a member to a group request serializer"""
    member_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
    )