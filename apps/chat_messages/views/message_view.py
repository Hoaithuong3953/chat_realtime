from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_messages.services import TextMessageService
from apps.chat_messages.serializers import SendMessageSerializer
from apps.chat_messages.dtos import SendMessageRequest

class MessageView(BaseApiView):
    def post(self, request, chat_id: UUID):
        """
        Handle send message to a chat request
        """
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = SendMessageRequest.model_validate(serializer.validated_data)

        result = TextMessageService.add_text_message(
            chat_id=chat_id,
            user_id=self.current_user.id,
            dto=dto,
        )

        return self.success_respone(
            message="Send message successfully.",
            data=result.model_dump(mode="json"),
        )