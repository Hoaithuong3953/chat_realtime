import pytest

from .constants import (
    LOGIN_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_USERNAME,
    INVALID_IDENTIFIER,
    SHORT_IDENTIFIER,
    SHORT_PASSWORD,
    WRONG_PASSWORD,
    HTTP_BAD_REQUEST,
    HTTP_FORBIDDEN,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    ACCESS_TOKEN_KEY,
    REFRESH_COOKIE_PATH,
    REFRESH_TOKEN_KEY,
    
)

@pytest.mark.django_db
class TestLoginView:
    def test_login_success_with_email(self, client, account):
        """Test that login succeeds with a valid email and sets the refresh token cookie"""
        payload = {
            "identifier": TEST_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_OK
        assert ACCESS_TOKEN_KEY in response.data["data"]
        assert response.data["data"][ACCESS_TOKEN_KEY]
        assert REFRESH_TOKEN_KEY not in response.data["data"]
        assert REFRESH_TOKEN_KEY in response.cookies

        cookie = response.cookies[REFRESH_TOKEN_KEY]

        assert cookie.value
        assert cookie["httponly"] is True
        assert cookie["path"] == REFRESH_COOKIE_PATH

    def test_login_success_with_username(self, client, account):
        """Test that login succeeds with a valid username and sets the refresh token cookie"""
        payload = {
            "identifier": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_OK
        assert response.data["data"][ACCESS_TOKEN_KEY]
        assert REFRESH_TOKEN_KEY in response.cookies

    def test_login_invalid_identifier(self, client):
        """Test that login returns unauthorized when the identifier is invalid"""
        payload = {
            "identifier": INVALID_IDENTIFIER,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_login_invalid_password(self, client, account):
        """Test that login returns unauthorized when the password is incorrect"""
        payload = {
            "identifier": TEST_EMAIL,
            "password": WRONG_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_login_disabled_account(self, client, account):
        """Test that login returns forbidden when the account is disabled"""
        account.is_active = False
        account.save(update_fields=["is_active"])

        payload = {
            "identifier": TEST_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_FORBIDDEN

    def test_login_missing_identifier(self, client):
        """Test that login returns bad request when the identifier is missing"""
        payload = {"password": TEST_PASSWORD}

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

    def test_login_missing_password(self, client):
        """Test that login returns bad request when the password is missing"""
        payload = {"identifier": TEST_EMAIL}

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

    def test_login_password_too_short(self, client):
        """Test that login returns bad request when the password is too short"""
        payload = {
            "identifier": TEST_EMAIL,
            "password": SHORT_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

    def test_login_identifier_too_short(self, client):
        """Test that login returns bad request when the identifier is too short"""
        payload = {
            "identifier": SHORT_IDENTIFIER,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            LOGIN_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST