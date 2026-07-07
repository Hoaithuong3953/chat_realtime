from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import LoginSerializer
from apps.users.services import AuthService
from apps.users.dto import LoginRequest
from shared.responses import APIResponse

class LoginView(APIView):
    """
    View for user login
    Public endpoint (No authentication required)
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Handle user login request"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_dto = AuthService.login(
            LoginRequest.model_validate(serializer.validated_data)
        )

        return Response(
            APIResponse.success(
                message="Login successfully.",
                data=response_dto.model_dump(mode="json"),
            ),
            status=HTTPStatus.OK,
        )