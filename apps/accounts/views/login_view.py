from rest_framework.permissions import AllowAny

from apps.accounts.serializers import LoginSerializer
from apps.accounts.services import LoginService
from apps.accounts.dtos import LoginRequest
from shared.security.cookie_service import CookieService
from shared.base_api_view import BaseApiView

class LoginView(BaseApiView):
    """
    View for user authentication
    Public endpoint (No authentication required)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user authentication request
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_dto = LoginService.login(
            LoginRequest.model_validate(serializer.validated_data)
        )

        response = self.success_respone(
            message="Login successfully.",
            data={"access_token": response_dto.access_token},
        )

        CookieService.set_refresh_token(
            response=response,
            refresh_token=response_dto.refresh_token,
        )

        return response