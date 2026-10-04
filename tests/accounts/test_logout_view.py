import pytest

from shared.env import settings
from apps.accounts.models import RefreshToken
from django.utils import timezone
from .constants import (
    HTTP_OK,
    INVALID_REFRESH_TOKEN,
    LOGOUT_URL,
    REFRESH_COOKIE_MAX_AGE_DELETED,
    REFRESH_COOKIE_PATH,
)

@pytest.mark.django_db
class TestLogoutView:
    def test_logout_success(
        self,
        client,
        account,
        refresh_token,
    ):
        """Test that logout revokes the refresh token and deletes the refresh cookie"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        response = client.post(
            LOGOUT_URL,
            format="json",
        )

        assert response.status_code == HTTP_OK

        token = RefreshToken.objects.get(account=account)

        assert token.revoked_at is not None
        assert settings.REFRESH_COOKIE_NAME in response.cookies

        cookie = response.cookies[settings.REFRESH_COOKIE_NAME]

        assert cookie["max-age"] == REFRESH_COOKIE_MAX_AGE_DELETED
        assert cookie["path"] == REFRESH_COOKIE_PATH

    def test_logout_without_cookie(self, client):
        """Test that logout succeeds and deletes the refresh cookie when no cookie is provided"""
        response = client.post(
            LOGOUT_URL,
            format="json",
        )

        assert response.status_code == HTTP_OK
        assert settings.REFRESH_COOKIE_NAME in response.cookies

        cookie = response.cookies[settings.REFRESH_COOKIE_NAME]

        assert cookie["max-age"] == REFRESH_COOKIE_MAX_AGE_DELETED
        assert cookie["path"] == REFRESH_COOKIE_PATH

    def test_logout_invalid_token(self, client):
        """Test that logout succeeds and deletes the refresh cookie for an invalid token"""
        client.cookies[settings.REFRESH_COOKIE_NAME] = INVALID_REFRESH_TOKEN

        response = client.post(
            LOGOUT_URL,
            format="json",
        )

        assert response.status_code == HTTP_OK
        assert settings.REFRESH_COOKIE_NAME in response.cookies

        cookie = response.cookies[settings.REFRESH_COOKIE_NAME]

        assert cookie["max-age"] == REFRESH_COOKIE_MAX_AGE_DELETED
        assert cookie["path"] == REFRESH_COOKIE_PATH

    def test_logout_revoked_token(
        self,
        client,
        account,
        refresh_token,
    ):
        """Test that logout succeeds without changing an already revoked refresh token"""
        token = RefreshToken.objects.get(account=account)

        token.revoked_at = timezone.now()
        token.save(update_fields=["revoked_at"])

        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh_token

        response = client.post(LOGOUT_URL, format="json")

        assert response.status_code == HTTP_OK

        token.refresh_from_db()

        assert token.revoked_at is not None