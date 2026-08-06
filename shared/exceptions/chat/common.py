from shared.exceptions.base.common import (
    NotFoundException,
    ForbiddenException,
)

class ChatNotFoundException(NotFoundException):
    """
    Exception raised when chat not found
    HTTP status code: 404 Not Found
    """
    error_code = "CHAT_NOT_FOUND"
    message = "Chat not found."

class ChatAccessDeniedException(ForbiddenException):
    """
    Exception raised when the user is not part of the chat
    HTTP status code: 403 Forbidden
    """
    error_code = "CHAT_ACCESS_DENIED"
    message = "You are not part of the chat."