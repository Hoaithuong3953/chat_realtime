import pytest

from apps.accounts.enums import Role
from .constants import (
    ACCOUNTS_URL,
    ADMIN_EMAIL,
    ADMIN_FULL_NAME,
    ADMIN_USERNAME,
    ACCOUNT_1_EMAIL,
    ACCOUNT_1_FULL_NAME,
    ACCOUNT_1_USERNAME,
    HTTP_BAD_REQUEST,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    NON_EXISTENT_ACCOUNT_ID,
    TEST_EMAIL,
    TEST_FULL_NAME,
    TEST_USERNAME,
)

@pytest.mark.django_db
class TestUpdateAccountView:
    def test_update_account_success_for_admin(self, client, account_factory):
        """Test that an admin can update an account successfully"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": False},
            format="json",
        )

        assert response.status_code == HTTP_OK

        data = response.json()["data"]

        assert data["id"] == str(account.id)
        assert data["is_active"] is False

        account.refresh_from_db()

        assert account.is_active is False

    def test_update_account_can_activate_inactive_account(self, client, account_factory):
        """Test that an admin can activate an inactive account"""
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
            is_active=False,
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": True},
            format="json",
        )

        assert response.status_code == HTTP_OK

        data = response.json()["data"]

        assert data["id"] == str(account.id)
        assert data["is_active"] is True

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_success_message(self, client, account_factory):
        """Test that updating an account returns a success message"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": False},
            format="json",
        )

        assert response.status_code == HTTP_OK
        assert response.json()["message"] == "Update account successfully."

    def test_update_account_unauthorized_without_authentication(self, client, account):
        """Test that updating an account requires authentication"""
        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": False},
            format="json",
        )

        assert response.status_code == HTTP_UNAUTHORIZED

    def test_update_account_forbidden_for_non_admin(self, client, account_factory):
        """Test that a non-admin cannot update another account"""
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

        response = client.patch(
            f"{ACCOUNTS_URL}{target_account.id}",
            {"is_active": False},
            format="json",
        )

        assert response.status_code == HTTP_FORBIDDEN

        target_account.refresh_from_db()

        assert target_account.is_active is True

    def test_update_account_returns_not_found_when_account_does_not_exist(
        self,
        client,
        account_factory,
    ):
        """Test that updating a non-existent account returns not found"""
        admin_account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{NON_EXISTENT_ACCOUNT_ID}",
            {"is_active": False},
            format="json",
        )

        assert response.status_code == HTTP_NOT_FOUND

    def test_update_account_returns_bad_request_when_is_active_is_missing(
        self,
        client,
        account_factory,
    ):
        """Test that a missing is_active field returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_bad_request_when_is_active_is_invalid_string(
        self,
        client,
        account_factory,
    ):
        """Test that an invalid string for is_active returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": "invalid"},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_bad_request_when_is_active_is_null(
        self,
        client,
        account_factory,
    ):
        """Test that a null value for is_active returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": None},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_bad_request_when_is_active_is_empty_string(
        self,
        client,
        account_factory,
    ):
        """Test that an empty string for is_active returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": ""},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_bad_request_when_is_active_is_integer(
        self,
        client,
        account_factory,
    ):
        """Test that an integer value for is_active returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": 123},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_bad_request_when_request_body_is_not_object(
        self,
        client,
        account_factory,
    ):
        """Test that a non-object request body returns bad request"""
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
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            [],
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_does_not_modify_account_when_validation_fails(
        self,
        client,
        account_factory,
    ):
        """Test that the account is not modified when validation fails"""
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
            is_active=False,
        )

        client.force_authenticate(user=admin_account)

        response = client.patch(
            f"{ACCOUNTS_URL}{account.id}",
            {"is_active": "invalid"},
            format="json",
        )

        assert response.status_code == HTTP_BAD_REQUEST

        account.refresh_from_db()

        assert account.is_active is False