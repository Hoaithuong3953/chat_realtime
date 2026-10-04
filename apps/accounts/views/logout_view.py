from rest_framework.permissions import AllowAny

from apps.accounts.services import LogoutService
from shared.env import settings
from shared.security.cookie_service import CookieService
from shared.base_api_view import BaseApiView

class LogoutView(BaseApiView):
    """
    Handle user logout requests
    Revoke the refresh token and clear the cookie
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user logout request"""
        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        LogoutService.logout(refresh_token)

        response = self.success_response(
            message="Logout successfully.",
        )

        CookieService.delete_refresh_token(response)

        return response