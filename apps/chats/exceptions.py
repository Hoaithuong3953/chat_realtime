from uuid import UUID

from shared.exceptions.common import (
    NotFoundException,
    ConflictException,
)

# Exception for create private chat
class TargetUserNotFoundException(NotFoundException):
    """
    Exception raised when target user does not exist
    HTTP status code: 404 Not Found
    """
    error_code = "USER_NOT_FOUND"
    message = "Target user not found."

class TargetUserInactiveException(NotFoundException):
    """
    Exception raised when target user is inactive and a new private chat cannot be created
    HTTP status code: 404 Not Found
    """
    error_code = "USER_INACTIVE"
    message = "Target user is inactive."

class SelfChatNotAllowedException(ConflictException):
    """
    Exception raised when create or access a private chat with yourself
    HTTP status code: 409 Conflict
    """
    error_code = "SELF_CHAT_NOT_ALLOWED"
    message = "Cannot create chat with yourself."

# Exception for group chat
class InvalidMemberException(NotFoundException):
    """
    Exception raised when member is invalid
    HTTP status code: 404 Not Found
    """
    error_code = "INVALID_MEMBERS"
    
    def __init__(self, member_ids: list[UUID], message: str):
        super().__init__(
            message=message,
            details={
                "member_ids": member_ids,
            }
        )