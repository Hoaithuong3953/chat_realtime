from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.services.auth_service import AuthService
from shared.responses import APIResponse
from apps.users.serializers import RegisterSerializer
from apps.users.dto import RegisterRequest

class RegisterView(APIView):
    """
    View for user registration
    Public endpoint (no authentication required)
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        """
        Handle user registration request
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RegisterRequest(**serializer.validated_data)
        response_dto = AuthService.register_user(request_dto)

        return Response(
            APIResponse.success(
                message="Register successfully.",
                data=response_dto.model_dump(mode="json"),
            ),
            status=HTTPStatus.CREATED
        )