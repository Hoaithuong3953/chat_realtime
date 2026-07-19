from uuid import UUID
from django.db import transaction

from apps.chats.dtos import CreatePrivateChatResponse, CreatePrivateChatRequest
from apps.chats.exceptions import (
    TargetUserInactiveException,
    TargetUserNotFoundException,
    SelfChatNotAllowedException,
)
from apps.chats.models import Chat, ChatParticipant
from apps.users.models import User

class PrivateChatService:
    
    @staticmethod
    @transaction.atomic
    def get_or_create(current_user, dto: CreatePrivateChatRequest) -> CreatePrivateChatResponse:
        """
        Get chat if it exists or create a new chat

        Raises:
            TargetUserNotFoundException: if target user not found
            TargetUserInactiveException: if target user is inactive
            SelfChatNotAllowedException: if create a private chat for yourself
        """
        target_user = User.objects.get_by_id(dto.target_user_id)

        if target_user is None:
            raise TargetUserNotFoundException()
        
        if not target_user.account.is_active:
            raise TargetUserInactiveException()
        
        if target_user.id == current_user.id:
            raise SelfChatNotAllowedException()
        
        chat = Chat.objects.get_private_chat(
            target_user.id,
            current_user.id,
        )

        if chat is None:
            chat = PrivateChatService._create_private_chat(
                current_user.id,
                target_user.id,
            )
            created = True
        else:
            created = False

        return CreatePrivateChatResponse(
            chat_id=chat.id,
            type=chat.type,
            created=created,
        )

    @staticmethod
    def _create_private_chat(user1_id: UUID, user2_id: UUID) -> Chat:
        """"""
        chat = Chat.objects.create_private_chat()

        ChatParticipant.objects.create_participants(
            chat_id=chat.id,
            user_ids=[user1_id, user2_id]
        )

        return chat