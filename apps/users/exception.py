from shared.exceptions.common import ConflictException, UnauthorizedException

class DuplicateUserException(ConflictException):
    """
    Exception raised when trying to register with existing email or username
    HTTP status code: 409 Conflict
    """
    error_code = "DUPLICATE_USER"

    def __init__(self, field: str):
        super().__init__(message=f"{field} already exists.")

class InvalidCredentialsException(UnauthorizedException):
    """
    Exception raised when login information is wrong
    HTTP status code: 401 Unauthorized
    """
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid email/username or password"