from shared.exceptions.base.common import (
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
)

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

class AccountDisabledException(ForbiddenException):
    """
    Exception raised when account is not active
    HTTP status code: 403 Forbidden
    """
    error_code = "ACCOUNT_DISABLED"
    message = "Account is disabled."

class AccountNotFoundException(NotFoundException):
    """
    Exception raised when account can not found
    HTTP status code: 404 Not Found
    """
    error_code = "ACCOUNT_NOT_FOUND"
    message = "Account not found."