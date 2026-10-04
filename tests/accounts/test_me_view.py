import pytest

from .constants import (
    AUTHORIZATION_TYPE,
    HTTP_UNAUTHORIZED,
    INVALID_ACCESS_TOKEN,
    ME_URL,
)

@pytest.mark.django_db
class TestMeView:
    def test_me_success(self, client, account, access_token):
        """Test that retrieving the current user returns a successful response with account data"""
        client.credentials(HTTP_AUTHORIZATION=f"{AUTHORIZATION_TYPE} {access_token}")

        response = client.get(ME_URL)

        assert response.status_code == 200

        data = response.json()["data"]

        assert data["id"] == str(account.id)
        assert data["email"] == account.email
        assert data["username"] == account.username
        assert data["role"] == account.role
        assert data["is_active"] is True
        assert "created_at" in data

    def test_me_without_authentication(self, client):
        """Test that retrieving the current user without authentication returns unauthorized"""
        response = client.get(ME_URL)

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_me_invalid_token(self, client):
        """Test that retrieving the current user with an invalid token returns unauthorized"""
        client.credentials(
            HTTP_AUTHORIZATION=f"{AUTHORIZATION_TYPE} {INVALID_ACCESS_TOKEN}",
        )

        response = client.get(ME_URL)

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_me_returns_current_user(self, client, account, access_token):
        """Test that retrieving the current user returns the authenticated user's ID"""
        client.credentials(HTTP_AUTHORIZATION=f"{AUTHORIZATION_TYPE} {access_token}")

        response = client.get(ME_URL)

        assert response.json()["data"]["id"] == str(account.id)