from django.http import HttpResponse

from shared.config.env import settings

class CookieService:
    """Service for managing authentication-related HTTP cookies"""

    @staticmethod
    def set_refresh_token(response: HttpResponse, refresh_token: str) -> None:
        """Set the refresh token as a HTTP-only cookie"""
        response.set_cookie(
            key=settings.REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=settings.REFRESH_COOKIE_SECURE,
            samesite=settings.REFRESH_COOKIE_SAMESITE,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60,
            path="/api/v1/auth",
        )