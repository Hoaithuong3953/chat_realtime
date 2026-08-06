from uuid import UUID

from apps.chats.models import Chat
from shared.exceptions.chat.common import ChatNotFoundException, ChatAccessDeniedException
from apps.chat_participants.models import ChatParticipant

class ChatConnectService:
    @staticmethod
    def validate_chat(
        chat_id: UUID,
        user_id: UUID,
    ) -> None:
        """Validate if the chat exists and if the user is a participant of the chat"""
        chat = Chat.objects.get_chat_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundException()

        is_participant = ChatParticipant.objects.is_participant(user_id=user_id, chat_id=chat_id)
        if not is_participant:
            raise ChatAccessDeniedException()