from shared.exceptions.base.app_exception import AppException

class AIException(AppException):
    """
    Base exception for AI provider errors
    """
    error_code = "AI_ERROR"
    message = "An AI service error occurred."

class AIProviderException(AIException):
    """
    Exception raised when the AI provider fails to process a request
    """
    error_code = "AI_PROVIDER_ERROR"
    message = "The AI service failed to process the request."