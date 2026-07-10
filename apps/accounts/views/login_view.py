from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.serializers import LoginSerializer
from apps.accounts.services import LoginService
from apps.accounts.dtos import LoginRequest
from shared.responses import APIResponse

class LoginView(APIView):
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

        return Response(
            APIResponse.success(
                message="Login successfully.",
                data=response_dto.model_dump(mode="json"),
            ),
            status=HTTPStatus.OK,
        )