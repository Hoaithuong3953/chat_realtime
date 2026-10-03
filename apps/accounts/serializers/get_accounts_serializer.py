from rest_framework import serializers

from apps.accounts.enums import Role

class GetAccountsSerializer(serializers.Serializer):
    q = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    role = serializers.ChoiceField(
        choices=Role.choices,
        required=False,
        allow_null=True,
    )
    is_active = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    page = serializers.IntegerField(
        required=False,
        min_value=1,
        default=1,
    )
    page_size = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        default=20,
    )

    def validate(self, attrs):
        attrs.setdefault("q", None)
        attrs.setdefault("role", None)
        attrs.setdefault("is_active", None)
        return attrs