from apps.accounts.dtos import MeResponse
from apps.accounts.models import Account
from shared.exceptions.auth import AccountNotFoundException

class MeService:

    @staticmethod
    def me(account_id: str) -> MeResponse:
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