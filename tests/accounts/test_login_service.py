from datetime import timedelta
from unittest.mock import patch
import pytest
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.dtos import LoginRequest
from apps.accounts.models import RefreshToken
from apps.accounts.services import LoginService
from shared.exceptions.auth import (
    AccountDisabledException,
    InvalidCredentialsException,
)
from shared.security import TokenHasher
from .constants import (
    INVALID_IDENTIFIER,
    OLD_REFRESH_TOKEN,
    REFRESH_TOKEN_EXPIRES_DAYS,
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_USERNAME,
    WRONG_PASSWORD,
)

@pytest.mark.django_db
class TestLoginService:
    def test_login_success_with_email(self, account):
        """Test that login succeeds when using a valid email and password"""
        dto = LoginRequest(
            identifier=TEST_EMAIL,
            password=TEST_PASSWORD,
        )

        before_login = timezone.now()

        response = LoginService.login(dto)

        account.refresh_from_db()

        assert response.access_token
        assert response.refresh_token

        token = AccessToken(response.access_token)

        assert str(token["user_id"]) == str(account.id)

        refresh_token = RefreshToken.objects.get(account=account)

        assert refresh_token.refresh_token == TokenHasher.hash_token(
            response.refresh_token
        )
        assert refresh_token.revoked_at is None
        assert refresh_token.expires_in > before_login

        assert account.last_login is not None
        assert account.last_login >= before_login

    def test_login_success_with_username(self, account):
        """Test that login succeeds when using a valid username and password"""
        dto = LoginRequest(
            identifier=TEST_USERNAME,
            password=TEST_PASSWORD,
        )

        response = LoginService.login(dto)

        assert response.access_token
        assert response.refresh_token

        token = AccessToken(response.access_token)

        assert str(token["user_id"]) == str(account.id)

        assert RefreshToken.objects.filter(account=account).exists()

    def test_login_invalid_identifier(self):
        """Test that login fails when the identifier does not match an account"""
        dto = LoginRequest(
            identifier=INVALID_IDENTIFIER,
            password=TEST_PASSWORD,
        )

        with pytest.raises(InvalidCredentialsException):
            LoginService.login(dto)

        assert not RefreshToken.objects.exists()

    def test_login_invalid_password(self):
        """Test that login fails when the password is incorrect"""
        dto = LoginRequest(
            identifier=TEST_EMAIL,
            password=WRONG_PASSWORD,
        )

        with pytest.raises(InvalidCredentialsException):
            LoginService.login(dto)

        assert not RefreshToken.objects.exists()

    def test_login_disabled_account(self, account):
        """Test that login fails when the account is disabled"""
        account.is_active = False
        account.save(update_fields=["is_active"])

        dto = LoginRequest(
            identifier=TEST_EMAIL,
            password=TEST_PASSWORD,
        )

        with pytest.raises(AccountDisabledException):
            LoginService.login(dto)

        assert not RefreshToken.objects.exists()

    def test_login_replaces_existing_refresh_token(self, account):
        """Test that login replaces an existing refresh token with a new one"""
        old_hash = TokenHasher.hash_token(OLD_REFRESH_TOKEN)

        RefreshToken.objects.create_token(
            account=account,
            refresh_token=old_hash,
            expires_in=timezone.now() + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS),
        )

        dto = LoginRequest(
            identifier=TEST_EMAIL,
            password=TEST_PASSWORD,
        )

        response = LoginService.login(dto)

        refresh_token = RefreshToken.objects.get(account=account)

        assert RefreshToken.objects.filter(account=account).count() == 1
        assert refresh_token.refresh_token != old_hash
        assert refresh_token.refresh_token == TokenHasher.hash_token(response.refresh_token)
        assert refresh_token.revoked_at is None

    @patch("apps.accounts.services.login_service.RefreshToken.objects.upsert_token")
    def test_login_refresh_token_error_rolls_back(self, mock_upsert_token, account):
        """Test that login rolls back last login and refresh token changes when token storage fails"""
        mock_upsert_token.side_effect = Exception("refresh token storage failed")

        dto = LoginRequest(
            identifier=TEST_EMAIL,
            password=TEST_PASSWORD,
        )

        with pytest.raises(Exception, match="refresh token storage failed"):
            LoginService.login(dto)

        account.refresh_from_db()

        assert RefreshToken.objects.filter(account=account).count() == 0
        assert account.last_login is None