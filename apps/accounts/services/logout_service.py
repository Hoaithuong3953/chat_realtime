from django.db import transaction

from apps.accounts.models import RefreshToken
from shared.security import TokenHasher

class LogoutService:

    @staticmethod
    @transaction.atomic
    def logout(refresh_token: str) -> None:
        RefreshToken.objects.revoke_by_hash(
            TokenHasher.hash_token(refresh_token)
        )