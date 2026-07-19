from apps.users.serializers.get_user_serializer import GetUsersSerializer
from apps.users.services.user_service import UserService
from apps.users.dtos.get_user_dto import GetUsersRequest
from shared.base_api_view import BaseApiView

class UserView(BaseApiView):
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

        return self.success_respone(
            message="Get users successfully.",
            data=result.model_dump(mode="json"),
        )