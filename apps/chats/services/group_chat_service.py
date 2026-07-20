from uuid import UUID

from django.db import transaction

from apps.chats.dtos import (
    CreateGroupChatRequest,
    CreateGroupChatResponse,
    UpdateGroupChatResponse,
    UpdateGroupChatRequest,
    GetGroupChatResponse,
)
from apps.chats.exceptions import (
    InvalidMemberException,
    ChatNotFoundException,
    AccessDeniedException,
    InvalidChatTypeException,
    InsufficientPermissionException,
)
from apps.users.user_models import User
from apps.chats.chat_models import Chat
from apps.chats.models.chat_participants_models import ChatParticipant
from apps.chats.enums import ChatType

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

    @staticmethod
    def get(chat_id: UUID, current_user_id: UUID) -> GetGroupChatResponse:
        """
        Get a exist group chat

        Raises:
            ChatNotFoundException: if the group chat does not exist
            AccessDeniedException: if a user is not a member of the group
            InvalidChatTypeException: if type of chat is not GROUP
        """
        chat = Chat.objects.get_chat_by_id(chat_id)

        if chat is None:
            raise ChatNotFoundException()
        
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()
        
        is_member = ChatParticipant.objects.is_member(
            chat_id=chat_id,
            user_id=current_user_id,
        )

        if is_member == False:
            raise AccessDeniedException()
        
        owner = ChatParticipant.objects.get_owner(chat_id=chat.id)
        member_count = ChatParticipant.objects.get_member_count(chat_id=chat.id)
        
        return GetGroupChatResponse(
            chat_id=chat.id,
            title=chat.title,
            avatar_url=chat.avatar_url or None,
            owner_id=owner.user_id,
            member_count=member_count,
            created_at=chat.created_at,
        )

    @staticmethod
    def update(chat_id: UUID, current_user_id: UUID, dto: UpdateGroupChatRequest) -> UpdateGroupChatResponse:
        """
        Update information for the group chat

        Raises:
            ChatNotFoundException: if the group chat does not exist
            InsufficientPermissionException: if user is not the owner of the group
            InvalidChatTypeException: if type of chat is not GROUP
        """
        chat = Chat.objects.get_chat_by_id(chat_id)

        if chat is None:
            raise ChatNotFoundException()
        
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()
        
        is_owner = ChatParticipant.objects.is_owner(
            chat_id=chat.id,
            user_id=current_user_id,
        )

        if not is_owner:
            raise InsufficientPermissionException()
        
        data = dto.model_dump(exclude_unset=True)
        chat = Chat.objects.update_group_chat_info(chat, **data)

        return UpdateGroupChatResponse.model_validate(chat)