from apps.accounts.services.me_service import MeService
from shared.base_api_view import BaseApiView

class MeView(BaseApiView):
    """
    Handle current account information requests
    Return information of the authenticated account
    """
    def get(self, request):
        """Handle get current account information request"""
        result = MeService.me(account_id=request.user.id)

        return self.success_response(
            message="Get current user successfully.",
            data=result.model_dump(mode="json"),
        )