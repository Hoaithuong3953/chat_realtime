from django.db import transaction

from apps.chats.dtos import (
    CreateGroupChatRequest,
    CreateGroupChatResponse,
    UpdateGroupChatResponse,
    UpdateGroupChatRequest,
    GetGroupChatResponse,
)
from apps.chats.exceptions import InvalidMemberException
from apps.users.models import User
from apps.chats.models.chat_models import Chat
from apps.chats.models.chat_participants_models import ChatParticipant

class GroupChatService:

    @staticmethod
    def create(current_user, dto: CreateGroupChatRequest) -> CreateGroupChatResponse:
        """
        Create a new chat with a group of people.

        Raises:
            InvalidMemberException: if user is not found, is inactive or adds themselves
        """
        active_members = User.objects.get_active_users_by_ids(dto.member_ids)

        active_ids = {member.id for member in active_members}
        invalid_ids = list(set(dto.member_ids) - active_ids)

        if current_user.id in dto.member_ids:
            raise InvalidMemberException(
                message="Cannot add yourself to the group chat.",
                member_ids=current_user.id,
            )

        if invalid_ids:
            raise InvalidMemberException(
                message="One or more members do not exist or are inactive.",
                member_ids=invalid_ids,
            )
        
        with transaction.atomic():
            chat = Chat.objects.create_group_chat(dto.title)

            ChatParticipant.objects.create_owner_participants(
                chat_id=chat.id,
                user_id=current_user.id
            )
            
            ChatParticipant.objects.create_participants(
                chat_id=chat.id,
                user_ids=active_ids,
            )
        
        return CreateGroupChatResponse(
            chat_id=chat.id,
            type=chat.type,
            title=chat.title,
            member_count=len(active_ids)+1,
        )