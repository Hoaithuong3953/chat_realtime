from apps.accounts.dtos import GetAccountsRequest
from apps.accounts.serializers import GetAccountsSerializer
from apps.accounts.services import AccountService
from shared.base_api_view import BaseApiView
from shared.security.permissions import IsAdmin

class AccountView(BaseApiView):
    """
    View for account listing
    Private endpoint (admin only)
    """
    permission_classes = [IsAdmin]
    def get(self, request):
        """Handle get account list request"""
        serializer = GetAccountsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

        result = AccountService.get_all(
            GetAccountsRequest.model_validate(
                serializer.validated_data,
            )
        )

        return self.success_response(
            message="Get accounts successfully.",
            data=result.model_dump(mode="json"),
        )