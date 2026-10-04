import pytest

from apps.accounts.enums import Role
from apps.accounts.services import AccountService
from shared.exceptions.auth.account import AccountNotFoundException
from .constants import (
    TEST_EMAIL,
    TEST_USERNAME,
    TEST_FULL_NAME,
    ADMIN_EMAIL,
    ADMIN_USERNAME,
    ADMIN_FULL_NAME,
    NON_EXISTENT_ACCOUNT_ID,
)

@pytest.mark.django_db
class TestUpdateAccountService:
    def test_update_account_sets_active_status_to_false(self, account_factory):
        """Test that an active account can be disabled"""
        account = account_factory(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            full_name=TEST_FULL_NAME,
            is_active=True,
        )

        result = AccountService.update_account(account_id=account.id, is_active=False)

        assert result.id == account.id
        assert result.is_active is False

        account.refresh_from_db()

        assert account.is_active is False

    def test_update_account_sets_active_status_to_true(self, account_factory):
        """Test that an inactive account can be activated"""
        account = account_factory(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            full_name=TEST_FULL_NAME,
            is_active=False,
        )

        result = AccountService.update_account(account_id=account.id, is_active=True)

        assert result.id == account.id
        assert result.is_active is True

        account.refresh_from_db()

        assert account.is_active is True

    def test_update_account_returns_updated_account(self, account_factory):
        """Test that the updated account information is returned"""
        account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )

        result = AccountService.update_account(account_id=account.id, is_active=False)

        assert result.id == account.id
        assert result.is_active is False

        account.refresh_from_db()

        assert account.is_active is False

    def test_update_account_raises_exception_when_account_not_found(self):
        """Test that an account not found exception is raised for a non-existent account"""
        with pytest.raises(AccountNotFoundException):
            AccountService.update_account(
                account_id=NON_EXISTENT_ACCOUNT_ID,
                is_active=False,
            )