from shared.exceptions.base.common import (
    NotFoundException,
    ForbiddenException,
    ValidationException,
    ConflictException,
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

class ReplyMessageNotFoundException(NotFoundException):
    """
    Exception raised when cannot find the replied messages
    HTTP status code: 404 Not Found
    """
    error_code = "REPLY_MESSAGE_NOT_FOUND"
    message = "Replied messages not found."

class InvalidCursorException(ValidationException):
    """
    Exception raised when the cursor is not in an invalid format
    HTTP status code: 400 Bad Request
    """
    error_code = "INVALID_CURSOR"
    message = "Invalid pagination cursor."

class MessageNotFoundException(NotFoundException):
    """
    Exception raised when cannot find the message
    HTTP status code: 404 Not Found
    """
    error_code = "MESSAGE_NOT_FOUND"
    message = "Messages not found."

class NoPermissionToRecallException(ForbiddenException):
    """
    Exception raised when the message is not sent by the user
    HTTP status code: 403 Forbidden
    """
    error_code = "NO_PERMISSION_TO_RECALL"
    message = "This message was not sent by you."

class MessageAlreadyRecalledException(ConflictException):
    """
    Exception raised when the message had been previously recalled
    HTTP status code: 409 Conflict
    """
    error_code = "MESSAGE_ALREADY_RECALLED"
    message = "This message already recalled."

class MessageRecallTimeExpiredException(ConflictException):
    """
    Exception raised when the message recall time limit has been expired
    HTTP status code: 409 Conflict
    """
    error_code = "MESSAGE_RECALL_TIME_EXPIRED"
    message = "The time limit for recalling the message has expired 5 minutes."