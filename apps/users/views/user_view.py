from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus

from apps.users.serializers.get_user_serializer import GetUsersSerializer
from apps.users.services.user_service import UserService
from apps.users.dtos.get_user_dto import GetUsersRequest
from shared.api_response import APIResponse

class UserView(APIView):
    """
    View for user listing
    Private endpoint (authentication required)
    """

    def get(self, request):
        """
        Handle user listing request
        """
        serializer = GetUsersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = UserService.get_all(
            GetUsersRequest.model_validate(
                serializer.validated_data
            )
        )

        return Response(
            APIResponse.success(
                message="Get users successfully.",
                data=result.model_dump(mode="json"),
            ),
            status=HTTPStatus.OK,
        )