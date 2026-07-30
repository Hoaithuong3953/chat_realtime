from uuid import UUID

from apps.chat_messages.models import Message
from apps.chat_participants.chat_participants_models import ChatParticipant
from apps.chats.chat_cursor import ChatCursor
from apps.chats.chat_models import Chat
from apps.chats.dtos import (
    ChatListItemResponse,
    GetChatListRequest,
    GetChatListResponse,
    LastMessageResponse,
    PaginationResponse,
)
from apps.chats.enums import ChatType

class ChatListService:
    @staticmethod
    def get(
        user_id: UUID,
        dto: GetChatListRequest,
    ) -> GetChatListResponse:
        """
        View the current user's paginated chat list
        """
        cursor = None

        if dto.before is not None:
            cursor = ChatCursor.decode(dto.before)

        chat_list = Chat.objects.get_chat_list(
            user_id=user_id,
            cursor=cursor,
            limit=dto.limit,
        )

        has_next = len(chat_list) > dto.limit

        if has_next:
            chat_list = chat_list[:dto.limit]

        next_cursor = None

        if has_next:
            last_chat = chat_list[-1]

            next_cursor = ChatCursor.encode(
                last_activity_at=last_chat.last_activity_at,
                chat_id=last_chat.id,
            )

        participants_by_chat = (
            ChatListService._get_other_participants(
                chat_list=chat_list,
                current_user_id=user_id,
            )
        )

        items = [
            ChatListService._build_chat_list_item(
                chat=chat,
                participant=participants_by_chat.get(chat.id),
            )
            for chat in chat_list
        ]

        return GetChatListResponse(
            items=items,
            pagination=PaginationResponse(
                has_next=has_next,
                next_cursor=next_cursor,
            ),
        )

    @staticmethod
    def _get_other_participants(
        chat_list: list[Chat],
        current_user_id: UUID,
    ) -> dict[UUID, ChatParticipant]:
        private_chat_ids = [
            chat.id
            for chat in chat_list
            if chat.type == ChatType.PRIVATE
        ]

        if not private_chat_ids:
            return {}

        participants = (
            ChatParticipant.objects.get_other_participants(
                chat_ids=private_chat_ids,
                current_user_id=current_user_id,
            )
        )

        return {
            participant.chat_id: participant
            for participant in participants
        }

    @staticmethod
    def _build_chat_list_item(
        chat: Chat,
        participant: ChatParticipant | None,
    ) -> ChatListItemResponse:
        other_participant = None

        if chat.type == ChatType.PRIVATE and participant is not None:
            title = participant.user.full_name
            avatar_url = participant.user.avatar_url
        else:
            title = chat.title
            avatar_url = chat.avatar_url

        return ChatListItemResponse(
            id=chat.id,
            type=chat.type,
            title=title,
            avatar_url=avatar_url or None,
            other_participant=other_participant,
            last_message=ChatListService._build_last_message(chat.last_message,),
            last_activity_at=chat.last_activity_at,
        )

    @staticmethod
    def _build_last_message(
        message: Message | None,
    ) -> LastMessageResponse | None:
        if message is None:
            return None

        return LastMessageResponse(
            id=message.id,
            sender_id=message.user_id,
            message_type=message.message_type,
            text_content=message.text_content,
            status=message.status,
            recalled_at=message.recalled_at,
            created_at=message.created_at,
        )
