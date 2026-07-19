from rest_framework.permissions import AllowAny

from apps.accounts.services import RefreshService
from shared.env import settings
from shared.security.cookie_service import CookieService
from shared.base_api_view import BaseApiView

class RefreshView(BaseApiView):

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle generate a new access token request"""
        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        result = RefreshService.refresh(
            refresh_token=refresh_token,
        )

        response = self.success_respone(
            message="Refresh token successfully.",
            data={
                "access_token": result.access_token
            },
        )

        CookieService.set_refresh_token(
            response=response,
            refresh_token=result.refresh_token,
        )

        return response