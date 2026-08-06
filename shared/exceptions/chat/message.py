from shared.exceptions.base.common import ConflictException, ForbiddenException, NotFoundException

class ReplyMessageNotFoundException(NotFoundException):
    """
    Exception raised when cannot find the replied messages
    HTTP status code: 404 Not Found
    """
    error_code = "REPLY_MESSAGE_NOT_FOUND"
    message = "Replied messages not found."

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