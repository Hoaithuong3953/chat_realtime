from http import HTTPStatus

from shared.base_api_view import BaseApiView
from apps.chats.dtos import CreateGroupChatRequest
from apps.chats.serializers import CreateGroupChatSerializer
from apps.chats.services import GroupChatService

class CreateGroupChatView(BaseApiView):
    """
    View for group chat creation
    Private endpoint (authentication required)
    """
    def post(self, request):
        """Handle create group chat request"""
        serializer = CreateGroupChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = CreateGroupChatRequest.model_validate(serializer.validated_data)

        result = GroupChatService.create(
            current_user=self.current_user,
            dto=dto,
        )

        return self.success_respone(
            message="Group chat created successfully.",
            data=result.model_dump(mode="json"),
            http_status=HTTPStatus.CREATED
        )