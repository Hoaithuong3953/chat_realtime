from http import HTTPStatus
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.services import RefreshService
from shared.responses.api_response import APIResponse
from shared.config.env import settings
from shared.security.cookie_service import CookieService


class RefreshView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        response_dto = RefreshService.refresh(
            refresh_token=refresh_token,
        )

        response = Response(
            APIResponse.success(
                message="Refresh token successfully.",
                data={
                    "access_token": response_dto.access_token
                },
            ),
            status=HTTPStatus.OK,
        )

        CookieService.set_refresh_token(
            response=response,
            refresh_token=response_dto.refresh_token,
        )

        return response