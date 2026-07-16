from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.accounts.services import LogoutService
from shared.api_response import APIResponse
from shared.env import settings
from shared.security.cookie_service import CookieService

class LogoutView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        LogoutService.logout(refresh_token)

        response = Response(
            APIResponse.success(
                message="Logout successfully.",
            ),
            status=HTTPStatus.OK,
        )

        CookieService.delete_refresh_token(response)

        return response