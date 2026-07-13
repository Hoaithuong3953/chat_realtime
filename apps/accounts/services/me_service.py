from apps.accounts.dtos import MeResponse
from apps.accounts.models import Account
from apps.accounts.exceptions import AccountNotFoundException

class MeService:

    @staticmethod
    def me(account_id: str) -> MeResponse:
        account = Account.objects.get_by_id_with_user(account_id)

        if account is None:
            raise AccountNotFoundException()
        
        return MeResponse(
            id=account.id,
            email=account.email,
            username=account.username,
            full_name=account.user_profile.full_name,
            role=account.role,
            is_active=account.is_active,
            created_at=account.created_at,
        )