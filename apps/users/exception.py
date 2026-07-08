from shared.exceptions.common import ConflictException, UnauthorizedException

class InvalidCredentialsException(UnauthorizedException):
    """
    Exception raised when login information is wrong
    HTTP status code: 401 Unauthorized
    """
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid email/username or password"