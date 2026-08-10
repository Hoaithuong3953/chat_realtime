from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_messages.services import FileMessageService
from apps.chat_messages.serializers import SendFileSerializer
from apps.chat_messages.dtos import SendFileMessageRequest

class FileMessageView(BaseApiView):
    def post(self, request, chat_id: UUID):
        """
        Handle send file messages to a chat request
        """
        serializer = SendFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = SendFileMessageRequest.model_validate(serializer.validated_data)

        result = FileMessageService.add_file_message(
            chat_id=chat_id,
            user_id=self.current_user.id,
            dto=dto,
        )

        return self.success_respone(
            message="Send document message successfully.",
            data=result.model_dump(mode="json"),
        )