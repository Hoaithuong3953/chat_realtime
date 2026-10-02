import httpx
from google.genai import errors

class AIRetryPolicy:
    
    @staticmethod
    def is_retryable(exception: Exception) -> bool:
        if isinstance(exception, errors.ServerError):
            return True

        if isinstance(exception, errors.ClientError):
            return exception.code == 429

        if isinstance(exception, httpx.TimeoutException):
            return True

        if isinstance(exception, httpx.NetworkError):
            return True

        return False