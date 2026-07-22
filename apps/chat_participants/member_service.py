from uuid import UUID
from django.db import transaction

from apps.chat_participants.dtos import (
    AddGroupMembersRequest,
    AddGroupMembersResponse,
    GetMembersListResponse,
    MemberItemResponse,
)
from apps.chats.chat_models import Chat
from apps.chat_participants.chat_participants_models import ChatParticipant
from apps.chat_participants.exceptions import (
    ChatNotFoundException,
    InvalidChatTypeException,
    AccessDeniedException,
    InsufficientPermissionException,
    MemberAlreadyExistsException,
    InvalidMemberException,
)
from apps.chats.enums import ChatType
from apps.users.user_models import User

class MemberService:

    @staticmethod
    def get_all(chat_id: UUID, user_id: UUID) -> GetMembersListResponse:
        """
        Get a list of members in the group chat

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

    @staticmethod
    def add_member(chat_id: UUID, user_id: UUID, dto: AddGroupMembersRequest) -> AddGroupMembersResponse:
        """
        Add a list of members in to the group chat

        Raises:
            InvalidMemberException: if user is not found, is inactive or adds themselves
            ChatNotFoundException: if the group chat does not exist
            InvalidChatTypeException: if type of chat is not GROUP
            InsufficientPermissionException: if user is not the owner of the group
            MemberAlreadyExistsException: if user is exists in the group
            InvalidMemberException: if member is not exist or is inactive
        """
        chat = Chat.objects.get_chat_by_id(chat_id)
        if chat is None:
            raise ChatNotFoundException()
        
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()

        is_owner = ChatParticipant.objects.is_owner(chat.id, user_id)

        if not is_owner:
            raise InsufficientPermissionException()
        
        active_members = User.objects.get_active_users()

        active_ids = {member.id for member in active_members}
        invalid_ids = list(set(dto.member_ids) - active_ids)

        if invalid_ids:
            raise InvalidMemberException(member_ids=invalid_ids)
        
        members = ChatParticipant.objects.get_existing_members(chat.id, dto.member_ids)
        existing_members = {m.user_id for m in members}

        if existing_members:
            raise MemberAlreadyExistsException(member_ids=existing_members)
        
        with transaction.atomic():
            ChatParticipant.objects.create_participants(
                chat_id=chat.id,
                user_ids=dto.member_ids,
            )

            member_count = ChatParticipant.objects.get_member_count(chat_id=chat.id)

        return AddGroupMembersResponse(
            id=chat.id,
            member_count=member_count,
        )