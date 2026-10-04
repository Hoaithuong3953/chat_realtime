import pytest

from apps.accounts.enums import Role
from apps.accounts.services.me_service import MeService
from shared.exceptions.auth import AccountNotFoundException
from .constants import (
    NON_EXISTENT_ACCOUNT_ID,
    UPDATED_USERNAME,
)

@pytest.mark.django_db
class TestMeService:
    def test_me_success(self, account):
        """Test that retrieving the current account returns the correct account data"""
        result = MeService.me(account_id=account.id)

        assert result.id == account.id
        assert result.email == account.email
        assert result.username == account.username
        assert result.role == Role.USER
        assert result.is_active is True
        assert result.created_at == account.created_at

    def test_me_account_not_found(self):
        """Test that retrieving a non-existent account raises an account not found exception"""
        with pytest.raises(AccountNotFoundException):
            MeService.me(account_id=NON_EXISTENT_ACCOUNT_ID)

    def test_me_returns_account_data(self, account):
        """Test that retrieving the account returns its updated data"""
        account.username = UPDATED_USERNAME
        account.save(update_fields=["username"])

        result = MeService.me(account_id=account.id)

        assert result.username == UPDATED_USERNAME