import secrets
from django.utils import timezone
from datetime import timedelta

from shared.env import settings

class RefreshTokenService:
    """Creates refresh tokens and manages their lifetime"""

    REFRESH_TOKEN_LIFETIME = timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    @staticmethod   
    def generate_refresh_token() -> str:
        """Generate a cryptographically secure refresh token"""
        return secrets.token_urlsafe(64)
    
    @classmethod
    def get_refresh_expiration(cls):
        """Return the refresh token expiration time"""
        return (timezone.now() + cls.REFRESH_TOKEN_LIFETIME)