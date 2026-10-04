from django.db import transaction

from apps.accounts.models import RefreshToken
from shared.security import TokenHasher

class LogoutService:
    """Service for logging out users"""

    @staticmethod
    @transaction.atomic
    def logout(refresh_token: str) -> None:
        """
        Revoke a refresh token
        Args:
            refresh_token: The refresh token to revoke
        """
        if not refresh_token:
            return
        
        RefreshToken.objects.revoke_by_hash(
            TokenHasher.hash_token(refresh_token)
        )