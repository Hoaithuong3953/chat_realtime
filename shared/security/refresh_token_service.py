import secrets
from django.utils import timezone

from shared.config.jwt import jwt_config

class RefreshTokenService:
    """Creates refresh tokens and manages their lifetime"""

    REFRESH_TOKEN_LIFETIME = jwt_config.refresh_lifetime

    @staticmethod   
    def generate_refresh_token() -> str:
        """Generate a cryptographically secure refresh token"""
        return secrets.token_urlsafe(64)
    
    @classmethod
    def get_refresh_expiration(cls):
        """Return the refresh token expiration time"""
        return (timezone.now() + cls.REFRESH_TOKEN_LIFETIME)