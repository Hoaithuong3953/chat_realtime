from uuid import UUID
from django.db import transaction, IntegrityError

from apps.chats.dtos import CreatePrivateChatResponse, CreatePrivateChatRequest
from apps.chats.exceptions import (
    TargetUserInactiveException,
    TargetUserNotFoundException,
    SelfChatNotAllowedException,
)
from apps.chats.models import Chat, ChatParticipant
from apps.users.user_models import User

class PrivateChatService:
    
    @staticmethod
    def get_or_create(current_user, dto: CreatePrivateChatRequest) -> CreatePrivateChatResponse:
        """
        Get chat if exists or create new chat between two users

        Raises:
            TargetUserNotFoundException: if target user not found
            TargetUserInactiveException: if target user is inactive
            SelfChatNotAllowedException: if create a private chat for yourself
        """
        target_user = User.objects.get_by_id(dto.target_user_id)

        key = PrivateChatService.generate_private_chat_key(target_user.id, current_user.id)

        if target_user is None:
            raise TargetUserNotFoundException()
        
        if not target_user.account.is_active:
            raise TargetUserInactiveException()
        
        if target_user.id == current_user.id:
            raise SelfChatNotAllowedException()
        
        try:
            with transaction.atomic():
                chat = Chat.objects.get_private_chat(private_key=key)
                if chat is None:
                    chat = PrivateChatService._create_private_chat(
                        current_user.id,
                        target_user.id,
                        private_key=key,
                    )
                    created = True
                else:
                    created = False

        except IntegrityError:
            chat = Chat.objects.get_private_chat(private_key=key)
            created = False

        return CreatePrivateChatResponse(
                chat_id=chat.id,
                type=chat.type,
                created=created,
            )

    @staticmethod
    def _create_private_chat(
        user1_id: UUID,
        user2_id: UUID,
        private_key,
    ) -> Chat:
        """Create a new private chat between two users"""
        chat = Chat.objects.create_private_chat(
            private_key=private_key,
        )

        ChatParticipant.objects.create_participants(
            chat_id=chat.id,
            user_ids=[user1_id, user2_id]
        )

        return chat
    
    @staticmethod
    def generate_private_chat_key(user1_id: UUID, user2_id: UUID) -> str:
        """Generate a key for a private chat between two users"""
        sorted_ids = sorted([
            str(user1_id),
            str(user2_id),
        ])

        return ":".join(sorted_ids)