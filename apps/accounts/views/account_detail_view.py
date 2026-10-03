from uuid import UUID

from apps.accounts.services import AccountService
from shared.base_api_view import BaseApiView
from shared.security.permissions import IsAdmin

class AccountDetailView(BaseApiView):
    permission_classes = [IsAdmin]
    
    def get(self, request, account_id: UUID):
        """Handle get account information request"""
        result = AccountService.get_account(account_id=account_id)

        return self.success_respone(
            message="Get account information successfully.",
            data=result.model_dump(mode="json"),
        )