import pytest

from apps.accounts.models import Account
from apps.users.models import User
from .constants import (
    EMAIL_ALREADY_EXISTS_ERROR_CODE,
    USERNAME_ALREADY_EXISTS_ERROR_CODE,
    HTTP_BAD_REQUEST,
    HTTP_CONFLICT,
    HTTP_CREATED,
    TEST_EMAIL,
    TEST_FULL_NAME,
    TEST_PASSWORD,
    TEST_USERNAME,
    EXISTING_EMAIL,
    EXISTING_USERNAME,
    NEW_EMAIL,
    NEW_USERNAME,
    REGISTER_URL,
    INVALID_EMAIL,
)

@pytest.mark.django_db
class TestRegisterView:
    def test_register_success(self, client):
        """Test that registration returns a successful response and creates the account"""
        payload = {
            "email": TEST_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
        }

        response = client.post(
            REGISTER_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_CREATED

        data = response.data["data"]

        assert data["email"] == TEST_EMAIL
        assert data["username"] == TEST_USERNAME
        assert data["full_name"] == TEST_FULL_NAME
        assert data["role"] == "USER"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

        assert Account.objects.filter(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
        ).exists()

        assert User.objects.filter(
            full_name=TEST_FULL_NAME,
        ).exists()

    def test_register_duplicate_email(self, client):
        """Test that registration returns a conflict when the email already exists"""
        Account.objects.create_account(
            email=TEST_EMAIL,
            username=EXISTING_USERNAME,
            password=TEST_PASSWORD,
        )

        payload = {
            "email": TEST_EMAIL,
            "username": NEW_USERNAME,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
        }

        response = client.post(
            REGISTER_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_CONFLICT
        assert response.data["error_code"] == EMAIL_ALREADY_EXISTS_ERROR_CODE

    def test_register_duplicate_username(self, client):
        """Test that registration returns a conflict when the username already exists"""
        Account.objects.create_account(
            email=EXISTING_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
        )

        payload = {
            "email": NEW_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
        }

        response = client.post(
            REGISTER_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_CONFLICT
        assert response.data["error_code"] == USERNAME_ALREADY_EXISTS_ERROR_CODE

    def test_register_invalid_email(self, client):
        """Test that registration returns a bad request for an invalid email"""
        payload = {
            "email": INVALID_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
        }

        response = client.post(
            REGISTER_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

    def test_register_missing_required_field(self, client):
        """Test that registration returns a bad request when a required field is missing"""
        payload = {
            "email": TEST_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }

        response = client.post(
            REGISTER_URL,
            payload,
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST