from uuid import UUID
from django.db import transaction

from apps.chat_participants.dtos import (
    AddGroupMembersRequest,
    AddGroupMembersResponse,
    GetMembersListResponse,
    MemberItemResponse,
    TransferOwnershipRequest,
)
from apps.chats.chat_models import Chat
from apps.chat_participants.chat_participants_models import ChatParticipant
from apps.chat_participants.exceptions import (
    GroupNotFoundException,
    InvalidChatTypeException,
    AccessDeniedException,
    NotGroupOwnerException,
    MemberAlreadyExistsException,
    InvalidMemberException,
    OwnerRequiredException,
    MemberNotFoundException,
    MemberAlreadyOwnerException,
)
from apps.chats.enums import ChatType
from apps.users.user_models import User

class MemberService:

    @staticmethod
    def get_all(chat_id: UUID, user_id: UUID) -> GetMembersListResponse:
        """
        Get a list of members in the group chat

        Raises:
            GroupNotFoundException: if the group chat does not exist
            AccessDeniedException: if a user is not a member of the group
            InvalidChatTypeException: if type of chat is not GROUP
        """
        chat = Chat.objects.get_chat_by_id(chat_id)
        if chat is None:
            raise GroupNotFoundException()
        
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
            GroupNotFoundException: if the group chat does not exist
            InvalidChatTypeException: if type of chat is not GROUP
            NotGroupOwnerException: if user is not the owner of the group
            MemberAlreadyExistsException: if user is exists in the group
            InvalidMemberException: if member is not exist or is inactive
        """
        chat = Chat.objects.get_chat_by_id(chat_id)
        if chat is None:
            raise GroupNotFoundException()
        
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()

        is_owner = ChatParticipant.objects.is_owner(chat.id, user_id)

        if not is_owner:
            raise NotGroupOwnerException()
        
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

    @staticmethod
    def delete_member(chat_id: UUID, current_user_id: UUID, member_id: UUID) -> None:
        """
        Delete a member from the group chat 

        Raises:
            GroupNotFoundException: if the group chat does not exist
            InvalidChatTypeException: if type of chat is not GROUP
            NotGroupOwnerException: if user is not the owner of the group
            OwnerRequiredException: if remove the last owner from the group
            MemberNotFoundException: if cannot find the member in the group
        """
        chat = Chat.objects.get_chat_by_id(chat_id)

        if chat is None:
            raise GroupNotFoundException()

        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()

        is_owner = ChatParticipant.objects.is_owner(chat.id, current_user_id)
        if not is_owner:
            raise NotGroupOwnerException()
        
        owner = ChatParticipant.objects.get_owner(chat.id)

        if owner and member_id==owner.user_id:
            raise OwnerRequiredException()

        with transaction.atomic():
            updated = ChatParticipant.objects.delete_member(
                chat_id=chat.id,
                member_id=member_id,
            )
            if updated == 0:
                raise MemberNotFoundException()

    @staticmethod
    def transfer_ownership(chat_id: UUID, current_user_id: UUID, dto: TransferOwnershipRequest) -> None:
        """
        Transfer group ownership to another member

        Raise:
            GroupNotFoundException: if the group chat does not exist
            InvalidChatTypeException: if type of chat is not GROUP
            NotGroupOwnerException: if user is not the owner of the group
            MemberNotFoundException: if cannot find the member in the group
            MemberAlreadyOwnerException: if member is already the group owner
        """
        chat = Chat.objects.get_chat_by_id(chat_id)

        # Check if the group is existing
        if chat is None:
            raise GroupNotFoundException()

        # Check if the chat is group
        if chat.type != ChatType.GROUP:
            raise InvalidChatTypeException()

        # Check if user is the owner of the group
        is_owner = ChatParticipant.objects.is_owner(chat.id, current_user_id)
        if not is_owner:
            raise NotGroupOwnerException()

        # Check if the select user is group member
        is_member = ChatParticipant.objects.is_member(chat.id, dto.new_owner_id)
        if not is_member:
            raise MemberNotFoundException()

        # Check if the member is already the group owner
        owner = ChatParticipant.objects.get_owner(chat.id)
        if owner and dto.new_owner_id==owner.user_id:
            raise MemberAlreadyOwnerException()

        with transaction.atomic():
            ChatParticipant.objects.transfer_ownership(
                chat_id=chat.id,
                current_owner_id=current_user_id,
                new_owner_id=dto.new_owner_id,
            )

    @staticmethod
    def leave(chat_id: UUID, current_member_id: UUID):
        """
        Allow a member to leave the group chat

        Raises:
            
        """