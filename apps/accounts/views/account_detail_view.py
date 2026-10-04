from uuid import UUID

from apps.accounts.services import AccountService
from apps.accounts.serializers import UpdateAccountSerializer
from shared.base_api_view import BaseApiView
from shared.security.permissions import IsAdmin

class AccountDetailView(BaseApiView):
    """
    Handle account detail requests
    Require admin authentication and permissions
    """
    permission_classes = [IsAdmin]
    
    def get(self, request, account_id: UUID):
        """Handle get account information request"""
        result = AccountService.get_account(account_id=account_id)

        return self.success_response(
            message="Get account information successfully.",
            data=result.model_dump(mode="json"),
        )

    def patch(self, request, account_id: UUID):
        """Handle update account request"""
        serializer = UpdateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AccountService.update_account(
            account_id=account_id,
            is_active=serializer.validated_data["is_active"],
        )

        return self.success_response(
            message="Update account successfully.",
            data=result.model_dump(mode="json"),
        )