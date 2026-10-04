import pytest

from apps.accounts.models import RefreshToken
from apps.accounts.services import LogoutService
from .constants import INVALID_REFRESH_TOKEN

@pytest.mark.django_db
class TestLogoutService:
    def test_logout_revokes_refresh_token(self, account, refresh_token):
        """Test that logout revokes the account's refresh token"""
        LogoutService.logout(refresh_token)

        token = RefreshToken.objects.get(account=account)

        assert token.revoked_at is not None

    def test_logout_does_not_delete_refresh_token(self, account, refresh_token):
        """Test that logout revokes the refresh token without deleting it"""
        LogoutService.logout(refresh_token)

        assert RefreshToken.objects.filter(
            account=account,
        ).count() == 1

    def test_logout_invalid_token_does_not_raise(self):
        """Test that logout silently ignores an invalid refresh token"""
        LogoutService.logout(INVALID_REFRESH_TOKEN)

        assert RefreshToken.objects.count() == 0

    def test_logout_revoked_token_is_idempotent(self, account, refresh_token):
        """Test that logging out with an already revoked token is idempotent"""
        LogoutService.logout(refresh_token)

        token = RefreshToken.objects.get(account=account)
        first_revoked_at = token.revoked_at

        LogoutService.logout(refresh_token)

        token.refresh_from_db()

        assert token.revoked_at is not None
        assert token.revoked_at >= first_revoked_at