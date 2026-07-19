from apps.accounts.services.me_service import MeService
from shared.base_api_view import BaseApiView

class MeView(BaseApiView):

    def get(self, request):
        """Handle get current account information request"""
        result = MeService.me(account_id=request.user.id)

        return self.success_respone(
            message="Get current user successfully.",
            data=result.model_dump(mode="json"),
        )