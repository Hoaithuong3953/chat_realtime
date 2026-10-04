import pytest

from apps.accounts.dtos import GetAccountResponse
from apps.accounts.enums import Role
from apps.accounts.services import AccountService
from shared.exceptions.auth.account import AccountNotFoundException
from .constants import (
    TEST_EMAIL,
    TEST_USERNAME,
    TEST_FULL_NAME,
    ACCOUNT_1_EMAIL,
    ACCOUNT_1_USERNAME,
    ACCOUNT_1_FULL_NAME,
    ACCOUNT_AVATAR_URL,
    INACTIVE_EMAIL,
    INACTIVE_USERNAME,
    INACTIVE_FULL_NAME,
    ADMIN_EMAIL,
    ADMIN_USERNAME,
    ADMIN_FULL_NAME,
    NON_EXISTENT_ACCOUNT_ID,
)

@pytest.mark.django_db
class TestGetAccountService:
    def test_get_account_returns_account_information(self, account_factory):
        """Test that account information is returned successfully"""
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
            avatar_url=ACCOUNT_AVATAR_URL,
        )

        result = AccountService.get_account(account_id=account.id)

        assert isinstance(result, GetAccountResponse)
        assert result.id == account.id
        assert result.email == ACCOUNT_1_EMAIL
        assert result.username == ACCOUNT_1_USERNAME
        assert result.role == Role.USER
        assert result.is_active is True
        assert result.full_name == ACCOUNT_1_FULL_NAME
        assert result.avatar_url == ACCOUNT_AVATAR_URL
        assert result.created_at == account.created_at
        assert result.updated_at == account.updated_at

    def test_get_account_returns_account_with_null_avatar_url(self, account_factory):
        """Test that account information is returned when avatar URL is null"""
        account = account_factory(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            full_name=TEST_FULL_NAME,
        )

        result = AccountService.get_account(account_id=account.id)

        assert result.id == account.id
        assert result.full_name == TEST_FULL_NAME
        assert result.avatar_url is None

    def test_get_account_returns_inactive_account(self, account_factory):
        """Test that an inactive account can be retrieved"""
        account = account_factory(
            email=INACTIVE_EMAIL,
            username=INACTIVE_USERNAME,
            full_name=INACTIVE_FULL_NAME,
            is_active=False,
        )

        result = AccountService.get_account(account_id=account.id)

        assert result.id == account.id
        assert result.email == INACTIVE_EMAIL
        assert result.username == INACTIVE_USERNAME
        assert result.is_active is False

    def test_get_account_returns_admin_account(self, account_factory):
        """Test that an admin account can be retrieved"""
        account = account_factory(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name=ADMIN_FULL_NAME,
            role=Role.ADMIN,
        )

        result = AccountService.get_account(account_id=account.id)

        assert result.id == account.id
        assert result.email == ADMIN_EMAIL
        assert result.username == ADMIN_USERNAME
        assert result.role == Role.ADMIN
        assert result.is_active is True
        assert result.full_name == ADMIN_FULL_NAME

    def test_get_account_raises_exception_when_account_not_found(self):
        """Test that an account not found exception is raised for a non-existent account"""
        with pytest.raises(AccountNotFoundException):
            AccountService.get_account(account_id=NON_EXISTENT_ACCOUNT_ID)