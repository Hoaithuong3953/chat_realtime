import pytest

from apps.accounts.enums import Role
from .constants import (
    TEST_EMAIL,
    TEST_USERNAME,
    TEST_FULL_NAME,
    ACCOUNT_1_EMAIL,
    ACCOUNT_1_USERNAME,
    ACCOUNT_1_FULL_NAME,
    ACCOUNT_AVATAR_URL,
    ADMIN_EMAIL,
    ADMIN_USERNAME,
    ADMIN_FULL_NAME,
    INACTIVE_EMAIL,
    INACTIVE_USERNAME,
    INACTIVE_FULL_NAME,
    ACCOUNTS_URL,
    NON_EXISTENT_ACCOUNT_ID,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
)

@pytest.mark.django_db
class TestGetAccountView:
    def test_get_account_success_for_admin(self, client, account_factory):
        """Test that an admin can retrieve account information successfully"""
        admin_account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
            avatar_url=ACCOUNT_AVATAR_URL,
        )

        client.force_authenticate(user=admin_account)

        response = client.get(f"{ACCOUNTS_URL}{account.id}")

        assert response.status_code == HTTP_OK

        data = response.json()

        assert data["data"]["id"] == str(account.id)
        assert data["data"]["email"] == ACCOUNT_1_EMAIL
        assert data["data"]["username"] == ACCOUNT_1_USERNAME
        assert data["data"]["role"] == Role.USER
        assert data["data"]["is_active"] is True
        assert data["data"]["full_name"] == ACCOUNT_1_FULL_NAME
        assert data["data"]["avatar_url"] == ACCOUNT_AVATAR_URL
        assert data["data"]["created_at"] == account.created_at.isoformat().replace("+00:00", "Z")
        assert data["data"]["updated_at"] == account.updated_at.isoformat().replace("+00:00", "Z")

    def test_get_account_success_with_null_avatar_url(self, client, account_factory):
        """Test that an admin can retrieve an account with a null avatar URL"""
        admin_account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )
        account = account_factory(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            full_name=TEST_FULL_NAME,
        )

        client.force_authenticate(user=admin_account)

        response = client.get(f"{ACCOUNTS_URL}{account.id}")

        assert response.status_code == HTTP_OK

        data = response.json()

        assert data["data"]["id"] == str(account.id)
        assert data["data"]["full_name"] == TEST_FULL_NAME
        assert data["data"]["avatar_url"] is None

    def test_get_account_returns_inactive_account_for_admin(
        self,
        client,
        account_factory,
    ):
        """Test that an admin can retrieve an inactive account"""
        admin_account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )
        account = account_factory(
            email=INACTIVE_EMAIL,
            username=INACTIVE_USERNAME,
            full_name=INACTIVE_FULL_NAME,
            is_active=False,
        )

        client.force_authenticate(user=admin_account)

        response = client.get(f"{ACCOUNTS_URL}{account.id}")

        assert response.status_code == HTTP_OK

        data = response.json()

        assert data["data"]["id"] == str(account.id)
        assert data["data"]["email"] == INACTIVE_EMAIL
        assert data["data"]["username"] == INACTIVE_USERNAME
        assert data["data"]["is_active"] is False

    def test_get_account_unauthorized_without_authentication(self, client, account):
        """Test that retrieving an account requires authentication"""
        response = client.get(f"{ACCOUNTS_URL}{account.id}")

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_get_account_forbidden_for_non_admin(self, client, account_factory):
        """Test that a non-admin cannot retrieve another account"""
        user_account = account_factory(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            full_name=TEST_FULL_NAME,
        )
        target_account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
        )

        client.force_authenticate(user=user_account)

        response = client.get(f"{ACCOUNTS_URL}{target_account.id}")

        assert response.status_code == HTTP_FORBIDDEN

    def test_get_account_returns_not_found_when_account_does_not_exist(
        self,
        client,
        account_factory,
    ):
        """Test that retrieving a non-existent account returns not found"""
        admin_account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )

        client.force_authenticate(user=admin_account)

        response = client.get(f"{ACCOUNTS_URL}{NON_EXISTENT_ACCOUNT_ID}")

        assert response.status_code == HTTP_NOT_FOUND