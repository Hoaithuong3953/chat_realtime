from shared.exceptions.common import ConflictException, UnauthorizedException

class EmailAlreadyExistsException(ConflictException):
    """
    Exception raised when trying to register with existing email
    HTTP status code: 409 Conflict
    """
    error_code = "EMAIL_ALREADY_EXISTS"
    message = "Email already exists."

class UsernameAlreadyExistsException(ConflictException):
    """
    Exception raised when trying to register with existing username
    HTTP status code: 409 Conflict
    """
    error_code = "USERNAME_ALREADY_EXISTS"
    message = "Username already exists."

class InvalidCredentialsException(UnauthorizedException):
    """
    Exception raised when login information is wrong
    HTTP status code: 401 Unauthorized
    """
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid email/username or password"