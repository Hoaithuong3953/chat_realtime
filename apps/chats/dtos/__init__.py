"""
Export DTOs for Chat module
"""
from .private_chat_dto import CreatePrivateChatRequest, CreatePrivateChatResponse
from .create_group_chat_dto import CreateGroupChatRequest, CreateGroupChatResponse

__all__ = [
    "CreatePrivateChatRequest",
    "CreatePrivateChatResponse",
    "CreateGroupChatRequest",
    "CreateGroupChatResponse",
]