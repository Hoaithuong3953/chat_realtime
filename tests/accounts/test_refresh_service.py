from datetime import timedelta
from unittest.mock import patch
import pytest
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import RefreshToken
from apps.accounts.services import RefreshService
from shared.exceptions.auth import InvalidRefreshTokenException
from shared.security import TokenHasher
from .constants import (
    EXPIRED_REFRESH_TOKEN,
    REFRESH_TOKEN_EXPIRED_SECONDS,
    REFRESH_TOKEN_EXPIRES_DAYS,
    INVALID_REFRESH_TOKEN,
    REVOKED_REFRESH_TOKEN,
)

@pytest.mark.django_db
class TestRefreshService:
    def test_refresh_success(self, account, refresh_token):
        """Test that refresh succeeds with a valid refresh token"""
        response = RefreshService.refresh(refresh_token)

        assert response.access_token
        assert response.refresh_token
        assert response.expires_in > 0

        access_token = AccessToken(response.access_token)

        assert str(access_token["user_id"]) == str(account.id)

    def test_refresh_empty_token(self):
        """Test that refresh fails when the refresh token is empty"""
        with pytest.raises(InvalidRefreshTokenException):
            RefreshService.refresh("")

    def test_refresh_token_not_found(self):
        """Test that refresh fails when the refresh token does not exist"""
        with pytest.raises(InvalidRefreshTokenException):
            RefreshService.refresh(INVALID_REFRESH_TOKEN)

    def test_refresh_revoked_token(self, account):
        """Test that refresh fails when the refresh token has been revoked."""
        RefreshToken.objects.create_token(
            account=account,
            refresh_token=TokenHasher.hash_token(REVOKED_REFRESH_TOKEN),
            expires_in=timezone.now() + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS),
        )

        RefreshToken.objects.filter(account=account).update(
            revoked_at=timezone.now(),
        )

        with pytest.raises(InvalidRefreshTokenException):
            RefreshService.refresh(REVOKED_REFRESH_TOKEN)

    def test_refresh_expired_token(self, account):
        """Test that refresh fails when the refresh token has expired"""
        RefreshToken.objects.create_token(
            account=account,
            refresh_token=TokenHasher.hash_token(EXPIRED_REFRESH_TOKEN),
            expires_in=timezone.now() - timedelta(
                seconds=REFRESH_TOKEN_EXPIRED_SECONDS,
            ),
        )

        with pytest.raises(InvalidRefreshTokenException):
            RefreshService.refresh(EXPIRED_REFRESH_TOKEN)

    def test_refresh_rotates_refresh_token(self, account, refresh_token):
        """Test that refresh rotates the existing refresh token and invalidates the old token"""
        old_hash = TokenHasher.hash_token(refresh_token)

        response = RefreshService.refresh(refresh_token)

        refresh = RefreshToken.objects.get(account=account)

        assert refresh.refresh_token != old_hash
        assert refresh.refresh_token == TokenHasher.hash_token(response.refresh_token)
        assert refresh.revoked_at is None

        with pytest.raises(InvalidRefreshTokenException):
            RefreshService.refresh(refresh_token)

    @patch("apps.accounts.services.refresh_service.RefreshToken.objects.rotate_token")
    def test_refresh_rotate_error_rolls_back(
        self,
        mock_rotate_token,
        account,
        refresh_token,
    ):
        """Test that refresh rolls back token rotation when token storage fails"""
        mock_rotate_token.side_effect = Exception("refresh token rotation failed")

        with pytest.raises(Exception, match="refresh token rotation failed"):
            RefreshService.refresh(refresh_token)

        refresh = RefreshToken.objects.get(account=account)

        assert refresh.refresh_token == TokenHasher.hash_token(refresh_token)
        assert refresh.revoked_at is None