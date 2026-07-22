from uuid import UUID

from apps.chat_participants.dtos import (
    GetMembersListResponse,
    MemberItemResponse,
)
from apps.chats.chat_models import Chat
from apps.chat_participants.chat_participants_models import ChatParticipant
from apps.chat_participants.exceptions import (
    ChatNotFoundException,
    InvalidChatTypeException,
    AccessDeniedException,
)
from apps.chats.enums import ChatType

class MemberService:

    @staticmethod
    def get_all(chat_id: UUID, user_id: UUID) -> GetMembersListResponse:
        """
        Get a list of members in the group chat

        Raises:
            InvalidMemberException: if user is not found, is inactive or adds themselves
        """
        chat = Chat.objects.get_chat_by_id(chat_id)
        if chat is None:
            raise ChatNotFoundException()
        
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()
        
        is_member = ChatParticipant.objects.is_member(chat.id, user_id)

        if not is_member:
            raise AccessDeniedException()
        
        members = ChatParticipant.objects.get_members_list(chat_id)
        
        return GetMembersListResponse(
            chat_id=chat.id,
            members=[
                MemberItemResponse(
                    id=member.user.id,
                    full_name=member.user.full_name,
                    avatar_url=member.user.avatar_url,
                    role=member.role,
                )
                for member in members
            ],
        )