from uuid import UUID

from apps.accounts.dtos import MeResponse
from apps.accounts.models import Account
from shared.exceptions.auth import AccountNotFoundException

class MeService:
    """Service for retrieving the authenticated user's information"""

    @staticmethod
    def me(account_id: UUID) -> MeResponse:
        """
        Get the authenticated user's account information

        Args:
            account_id: The account ID

        Returns:
            The account information

        Raises:
            AccountNotFoundException: If the account does not exist
        """
        account = Account.objects.get_by_id(account_id)

        if account is None:
            raise AccountNotFoundException()
        
        return MeResponse(
            id=account.id,
            email=account.email,
            username=account.username,
            role=account.role,
            is_active=account.is_active,
            created_at=account.created_at,
        )