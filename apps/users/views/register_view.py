from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.services.auth_service import AuthService
from shared.responses import APIResponse
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
        dto = RegisterRequest(**request.data)

        user_data = AuthService.register_user(dto)
        return Response(
            APIResponse.success(
                message="Register successfully.",
                data=user_data
            ),
            status=201
        )