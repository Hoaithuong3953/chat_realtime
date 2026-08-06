from shared.exceptions.base.common import ValidationException

class InvalidCursorException(ValidationException):
    """
    Exception raised when the cursor is not in an invalid format
    HTTP status code: 400 Bad Request
    """
    error_code = "INVALID_CURSOR"
    message = "Invalid pagination cursor."