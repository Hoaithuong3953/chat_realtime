from uuid import UUID

from shared.exceptions.common import (
    NotFoundException,
    ConflictException,
    ForbiddenException,
)

class InvalidMemberException(NotFoundException):
    """
    Exception raised when member is invalid
    HTTP status code: 404 Not Found
    """
    error_code = "INVALID_MEMBERS"
    message = "One or more members do not exist or are inactive."

    def __init__(self, *, member_ids: list[UUID]):
        super().__init__(
            details={
                "member_ids": member_ids,
            }
        )

class ChatNotFoundException(NotFoundException):
    """
    Exception raised when group chat not found
    HTTP status code: 404 Not Found
    """
    error_code = "CHAT_NOT_FOUND"
    message = "Group chat not found."

class AccessDeniedException(ForbiddenException):
    """
    Exception raised when user is not a member of group chat
    HTTP status code: 403 Forbidden
    """
    error_code = "ACCESS_DENIED"
    message = "You are not a member of this group."

class InvalidChatTypeException(ConflictException):
    """
    Exception raised when type of chat is wrong
    HTTP status code: 409 Conflict
    """
    error_code = "INVALID_CHAT_TYPE"
    message = "This operation is only supported for group chats."

class InsufficientPermissionException(ForbiddenException):
    """
    Exception raised when the user does not have permission to update the group
    HTTP status code: 403 Forbidden
    """
    error_code = "INSUFFICIENT_PERMISSION"
    message = "Only owner can update group information."

class MemberAlreadyExistsException(ConflictException):
    """
    Exception raised when the user already exists in the group
    HTTP status code: 409 Conflict
    """
    error_code = "MEMBER_ALREADY_EXISTS"
    message = "One or more users are already group members."

    def __init__(self, *, member_ids: list[UUID]):
        super().__init__(
            details={
                "member_ids": member_ids,
            }
        )

class OwnerRequiredException(ConflictException):
    """
    Exception raised when remove the last owner from the group.
    HTTP status code: 409 Conflict
    """
    error_code = "OWNER_REQUIRED"
    message = "Cannot remove the last owner from the group."