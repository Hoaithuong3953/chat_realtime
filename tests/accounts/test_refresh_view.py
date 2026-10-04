import pytest

from apps.accounts.models import RefreshToken
from shared.env import settings
from shared.security import TokenHasher
from .constants import (
    ACCESS_TOKEN_KEY,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    INVALID_REFRESH_TOKEN,
    REFRESH_COOKIE_PATH,
    REFRESH_TOKEN_EXPIRED_SECONDS,
    REFRESH_TOKEN_KEY,
    REFRESH_TOKEN_EXPIRES_DAYS,
    REFRESH_URL,
    REVOKED_REFRESH_TOKEN,
    EXPIRED_REFRESH_TOKEN,
    EXPIRES_IN_KEY,
)

@pytest.mark.django_db
class TestRefreshView:
    def test_refresh_success(self, client, account, refresh_token):
        """Test that refresh succeeds with a valid token and rotates the refresh cookie"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert response.status_code == HTTP_OK

        data = response.data["data"]

        assert data[ACCESS_TOKEN_KEY]
        assert data[EXPIRES_IN_KEY] > 0
        assert REFRESH_TOKEN_KEY not in data
        assert settings.REFRESH_COOKIE_NAME in response.cookies

        cookie = response.cookies[settings.REFRESH_COOKIE_NAME]

        assert cookie.value
        assert cookie.value != refresh_token
        assert cookie["httponly"] is True
        assert cookie["path"] == REFRESH_COOKIE_PATH

        refresh = RefreshToken.objects.get(account=account)

        assert refresh.refresh_token == TokenHasher.hash_token(cookie.value)
        assert refresh.revoked_at is None

    def test_refresh_without_cookie(self, client):
        """Test that refresh returns unauthorized when the refresh cookie is missing"""
        response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED
        assert not response.cookies

    def test_refresh_invalid_token(self, client):
        """Test that refresh returns unauthorized when the refresh token is invalid"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = INVALID_REFRESH_TOKEN

        response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED
        assert not response.cookies

    def test_refresh_expired_token(self, client, account):
        """Test that refresh returns unauthorized when the refresh token has expired"""
        from django.utils import timezone
        from apps.accounts.models import RefreshToken
        from shared.security import TokenHasher

        RefreshToken.objects.create_token(
            account=account,
            refresh_token=TokenHasher.hash_token(EXPIRED_REFRESH_TOKEN),
            expires_in=timezone.now() - timezone.timedelta(
                seconds=REFRESH_TOKEN_EXPIRED_SECONDS,
            ),
        )

        client.cookies[settings.REFRESH_COOKIE_NAME] = EXPIRED_REFRESH_TOKEN

        response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED
        assert not response.cookies

    def test_refresh_revoked_token(self, client, account):
        """Test that refresh returns unauthorized when the refresh token has been revoked"""
        from django.utils import timezone
        from apps.accounts.models import RefreshToken
        from shared.security import TokenHasher

        RefreshToken.objects.create_token(
            account=account,
            refresh_token=TokenHasher.hash_token(REVOKED_REFRESH_TOKEN),
            expires_in=timezone.now() + timezone.timedelta(
                days=REFRESH_TOKEN_EXPIRES_DAYS,
            ),
        )

        RefreshToken.objects.filter(account=account).update(
            revoked_at=timezone.now(),
        )

        client.cookies[settings.REFRESH_COOKIE_NAME] = REVOKED_REFRESH_TOKEN

        response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED
        assert not response.cookies

    def test_refresh_old_token_cannot_be_reused(self, client, refresh_token):
        """Test that the old refresh token cannot be reused after rotation"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        first_response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert first_response.status_code == HTTP_OK

        new_refresh_token = first_response.cookies[
            settings.REFRESH_COOKIE_NAME
        ].value

        assert new_refresh_token != refresh_token

        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        second_response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert second_response.status_code == HTTP_UNAUTHORIZED

    def test_refresh_new_token_can_be_used_again(self, client, refresh_token):
        """Test that the newly rotated refresh token can be used again"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        first_response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert first_response.status_code == HTTP_OK

        new_refresh_token = first_response.cookies[settings.REFRESH_COOKIE_NAME].value

        client.cookies[settings.REFRESH_COOKIE_NAME] = new_refresh_token

        second_response = client.post(
            REFRESH_URL,
            format="json",
        )

        assert second_response.status_code == HTTP_OK
        assert second_response.data["data"][ACCESS_TOKEN_KEY]
        assert second_response.data["data"][EXPIRES_IN_KEY] > 0