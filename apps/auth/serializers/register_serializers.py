from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration data validation

    Fields:
    - email: User's email address
    - username: User's username
    - password: User's password
    - name: User's display name
    """
    email = serializers.EmailField(
        max_length=255,
    )
    username = serializers.CharField(
        max_length=50,
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    name = serializers.CharField(
        max_length=100,
    )