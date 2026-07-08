from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.accounts.services import RegisterService
from shared.responses import APIResponse
from apps.accounts.serializers import RegisterSerializer
from apps.accounts.dtos import RegisterRequest

class RegisterView(APIView):
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

        return Response(
            APIResponse.success(
                message="Register successfully.",
                data=response_dto.model_dump(mode="json"),
            ),
            status=HTTPStatus.CREATED,
        )