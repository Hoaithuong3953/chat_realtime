from http import HTTPStatus
from rest_framework.permissions import AllowAny

from apps.accounts.services import RegisterService
from apps.accounts.serializers import RegisterSerializer
from apps.accounts.dtos import RegisterRequest
from shared.base_api_view import BaseApiView

class RegisterView(BaseApiView):
    """
    View for user registration
    Public endpoint (no authentication required)
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle user registration request
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_dto = RegisterService.register(
            RegisterRequest.model_validate(serializer.validated_data)
        )

        return self.success_respone(
            message="Register successfully.",
            data=response_dto.model_dump(mode="json"),
            http_status=HTTPStatus.CREATED,
        )