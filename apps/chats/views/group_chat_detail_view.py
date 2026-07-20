from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chats.dtos import UpdateGroupChatRequest
from apps.chats.serializers import UpdateGroupChatSerializer
from apps.chats.services import GroupChatService

class GroupChatDetailView(BaseApiView):
    """
    View for group chat detail
    Private endpoint (authentication required)
    """
    def get(self, request, chat_id: UUID):
        """Handle get group chat information request"""
        result = GroupChatService.get(
            chat_id=chat_id,
            current_user_id=self.current_user,
        )

        return self.success_respone(
            message="Group information retrieved successfully.",
            data=result.model_dump(mode="json"),
        )

    def patch(self, request, chat_id: UUID):
        """Handle update group chat information request"""
        serializer = UpdateGroupChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = UpdateGroupChatRequest.model_validate(serializer.validated_data)

        result = GroupChatService.update(
            chat_id=chat_id,
            current_user_id=self.current_user,
            dto=dto,
        )

        return self.success_respone(
            message="Group information updated successfully.",
            data=result.model_dump(mode="json"),
        )