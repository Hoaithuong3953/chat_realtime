from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_messages.services import MessageService

class MessageRecallView(BaseApiView):

    def post(self, request, chat_id: UUID, message_id: UUID):
        """
        Handle recall message request
        """
        result = MessageService.recall_message(
            chat_id=chat_id,
            user_id=self.current_user.id,
            message_id=message_id,
        )

        return self.success_respone(
            message="Recall message successfully.",
            data=result.model_dump(mode="json"),
        )