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
    AccessDeniedException,
    NotGroupOwnerException,
    MemberAlreadyExistsException,
    InvalidUserException,
    OwnerRequiredException,
    MemberNotFoundException,
    MemberAlreadyOwnerException,
    OwnerMustTransferException,
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

        # Check if group chat is exist
        if not chat or chat.type != ChatType.GROUP:
            raise GroupNotFoundException()
        
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

        # Check if the group is exist
        if not chat or chat.type != ChatType.GROUP:
            raise GroupNotFoundException()

        # Check if user is the owner of the group
        is_owner = ChatParticipant.objects.is_owner(chat.id, user_id)
        if not is_owner:
            raise NotGroupOwnerException()

        # Check if the user is inactive or is invalid
        active_users = User.objects.get_active_users()
        active_ids = {member.id for member in active_users}
        invalid_ids = list(set(dto.member_ids) - active_ids)
        if invalid_ids:
            raise InvalidUserException(member_ids=invalid_ids)

        # Check if members is active in group
        active_members = ChatParticipant.objects.get_active_members(chat.id, dto.member_ids)
        active_ids = {m.user_id for m in active_members}
        if active_ids:
            raise MemberAlreadyExistsException(member_ids=active_ids)

        # Get list if the user has previously joined the group
        inactive_members = ChatParticipant.objects.get_inactive_members(chat.id, dto.member_ids)
        inactive_ids = {m.user_id for m in inactive_members}

        new_member_ids = [
            member_id for member_id in dto.member_ids
            if member_id not in inactive_ids
        ] 
        
        with transaction.atomic():
            # Add the user has previously joined the group
            if inactive_ids:
                ChatParticipant.objects.rejoin_members(chat.id, list(inactive_ids))

            # Add the new users as group members
            if new_member_ids:
                ChatParticipant.objects.create_participants(
                    chat_id=chat.id,
                    user_ids=dto.member_ids,
                )

            member_count = ChatParticipant.objects.get_member_count(chat_id=chat.id)
            Chat.objects.update_timestamp(chat.id)

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

        # Check if group chat is exist
        if not chat or chat.type != ChatType.GROUP:
            raise GroupNotFoundException()

        # Check if the user is not owner
        is_owner = ChatParticipant.objects.is_owner(chat.id, current_user_id)
        if not is_owner:
            raise NotGroupOwnerException()

        # Check if the target id is duplicate the owner
        owner = ChatParticipant.objects.get_owner(chat.id)
        if owner and member_id==owner.user_id:
            raise OwnerRequiredException()

        with transaction.atomic():
            updated = ChatParticipant.objects.leave_member(
                chat_id=chat.id,
                member_id=member_id,
            )
            if updated == 0:
                raise MemberNotFoundException()

            Chat.objects.update_timestamp(chat.id)

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
        if not chat or chat.type != ChatType.GROUP:
            raise GroupNotFoundException()

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

            Chat.objects.update_timestamp(chat.id)

    @staticmethod
    def leave(chat_id: UUID, current_member_id: UUID) -> None:
        """
        Allow a member to leave the group chat

        Raises:
            GroupNotFoundException: if the group chat does not exist
            InvalidChatTypeException: if type of chat is not GROUP
            MemberNotFoundException: if cannot find the member in the group
            OwnerMustTransferException: if user is owner and wants to leave group
        """
        chat = Chat.objects.get_chat_by_id(chat_id)

        # Check if the group is exist
        if not chat or chat.type != ChatType.GROUP:
            raise GroupNotFoundException()

        # Check if the user is a member of the group
        is_member = ChatParticipant.objects.is_member(chat.id, current_member_id)
        if not is_member:
            raise MemberNotFoundException()

        # Check if the user is already the group owner
        is_owner = ChatParticipant.objects.is_owner(chat.id, current_member_id)
        if is_owner:
            raise OwnerMustTransferException()

        with transaction.atomic():
            ChatParticipant.objects.leave_member(chat_id, current_member_id)
            Chat.objects.update_timestamp(chat.id)