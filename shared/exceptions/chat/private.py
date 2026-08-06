from shared.exceptions.base.common import ConflictException

class SelfChatNotAllowedException(ConflictException):
    """
    Exception raised when create or access a private chat with yourself
    HTTP status code: 409 Conflict
    """
    error_code = "SELF_CHAT_NOT_ALLOWED"
    message = "Cannot create chat with yourself."