from http import HTTPStatus
from typing import Any

class AppException(Exception):
    """
    Base exception class for application-specific errors.
    This class can be extended to create more specific exceptions with custom error codes, messages and HTTP status codes

    Attributes:
        error_code (str): A unique error code for the exception
        message (str): A human-readable error message
        http_status (HTTPStatus): An HTTP status code associated with the exception, used for API responses

    Instance attributes:
        details (dict):  additional details about the error (Optional)
    """
    error_code: str = "INTERNAL_ERROR"
    message: str = "An internal error occurred. Please try again later."
    http_status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        if message is not None:
            self.message = message

        self.details = details if details is not None else {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }