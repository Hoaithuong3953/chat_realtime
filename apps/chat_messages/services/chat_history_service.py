from uuid import UUID

from apps.chat_messages.dtos import (
    GetChatHistoryRequest,
    GetChatHistoryResponse,
    MessageResponse,
    PaginationResponse,
    DocumentResponse,
)
from apps.chat_messages.exceptions import ChatAccessDeniedException, ChatNotFoundException
from apps.chats.models import Chat
from apps.chat_participants.models import ChatParticipant
from apps.chat_messages.message_cursor import MessageCursor
from apps.chat_messages.models import Message
from apps.chat_messages.enums import MessageType

class ChatHistoryService:

    @staticmethod
    def get(dto: GetChatHistoryRequest, chat_id: UUID, user_id: UUID) -> GetChatHistoryResponse:
        """
        Get paginated message history of a chat
        
        Raises:
            ChatAccessDeniedException: if the user is not part of the chat
            ChatNotFoundException: if chat not found
            InvalidCursorException: if cursor is not in an invalid format
        """
        chat = Chat.objects.get_chat_by_id(chat_id=chat_id)

        # Check if the chat is exist
        if chat is None:
            raise ChatNotFoundException()

        # Check if the user is a participant of chat
        is_participant = ChatParticipant.objects.is_participant(chat_id, user_id)
        if not is_participant:
            raise ChatAccessDeniedException()

        # Decode the pagination cursor to determine where to continue loading history
        cursor = None
        if dto.before is not None:
            cursor = MessageCursor.decode(dto.before)

        # Fetch one extra record to determine whether another page exists
        messages_list = Message.objects.get_chat_history(
            chat_id=chat.id,
            cursor=cursor,
            limit=dto.limit + 1,
        )

        # Remove the extra record before returning the response
        has_next = len(messages_list) > dto.limit
        if has_next:
            messages_list = messages_list[:dto.limit]

        # Generate the cursor from the last returned message
        next_cursor = None
        if has_next:
            last_message = messages_list[-1]
            next_cursor = MessageCursor.encode(
                created_at=last_message.created_at,
                message_id=last_message.id,
            )

        responses: list[MessageResponse] = []
        for message in messages_list:
            document = None
            if message.message_type == MessageType.DOCUMENT:
                document = DocumentResponse(
                    file_asset_id=message.document_message.file_asset_id,
                    original_name=message.document_message.file_asset.original_name,
                    file_size=message.document_message.file_asset.file_size,
                )

            responses.append(
                MessageResponse(
                    id=message.id,
                    user=message.user_id,
                    chat=message.chat_id,
                    text_content=message.text_content,
                    document=document,
                    status=message.status,
                    message_type=message.message_type,
                    created_at=message.created_at,
                    recalled_at=message.recalled_at,
                )
            )

        return GetChatHistoryResponse(
            messages=responses,
            pagination=PaginationResponse(
                has_next=has_next,
                next_cursor=next_cursor,
            )
        )