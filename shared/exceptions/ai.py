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

class UnsupportedAIProviderException(AIException):
    """
    Exception raised when AI provider is not supported
    """
    error_code = "UNSUPPORTED_AI_PROVIDER"
    message = "The configured AI provider is not supported."

    def __init__(self, *, provider: str):
        super().__init__(
            details={
                "provider": provider,
            }
        )