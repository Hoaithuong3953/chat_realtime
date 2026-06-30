from http import HTTPStatus
from typing import Any

class AppException(Exception):
    """
    Base exception class for application-specific errors.
    This class can be extended to create more specific exceptions 
    with custom error codes, messages and HTTP status codes

    Attributes:
        error_code (str): A unique error code for the exception
        message (str): A human-readable error message
        http_status (HTTPStatus): An HTTP status code associated with the exception, used for API responses
        details (dict): Optional additional details about the error
    """
    error_code: str
    message: str
    http_status: HTTPStatus | None = None

    def __init__(
        self,
        message: str | None = None,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details
        super().__init__(self.message)