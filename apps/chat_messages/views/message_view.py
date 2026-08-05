from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_messages.services import TextMessageService, ChatHistoryService
from apps.chat_messages.serializers import SendMessageSerializer, GetChatHistorySerializer
from apps.chat_messages.dtos import SendTextMessageRequest, GetChatHistoryRequest

class MessageView(BaseApiView):
    def post(self, request, chat_id: UUID):
        """
        Handle send message to a chat request
        """
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = SendTextMessageRequest.model_validate(serializer.validated_data)

        result = TextMessageService.add_text_message(
            chat_id=chat_id,
            user_id=self.current_user.id,
            dto=dto,
        )

        return self.success_respone(
            message="Send message successfully.",
            data=result.model_dump(mode="json"),
        )

    def get(self, request, chat_id: UUID):
        serializer = GetChatHistorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        dto = GetChatHistoryRequest.model_validate(serializer.validated_data)
        result = ChatHistoryService.get(
            dto=dto,
            chat_id=chat_id,
            user_id=self.current_user.id,
        )

        return self.success_respone(
            message="Get chat history sucessfully.",
            data=result.model_dump(mode="json"),
        )