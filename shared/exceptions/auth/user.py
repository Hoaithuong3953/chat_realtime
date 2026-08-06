from uuid import UUID
from shared.exceptions.base.common import NotFoundException

class UserNotFoundException(NotFoundException):
    """
    Exception raised when user does not exist
    HTTP status code: 404 Not Found
    """
    error_code = "USER_NOT_FOUND"
    message = "User not found."

class UserInactiveException(NotFoundException):
    """
    Exception raised when user is inactive and a new private chat cannot be created
    HTTP status code: 404 Not Found
    """
    error_code = "USER_INACTIVE"
    message = "User is inactive."

class InvalidUserException(NotFoundException):
    """
    Exception raised when user is invalid or inactive
    HTTP status code: 404 Not Found
    """
    error_code = "INVALID_USERS"
    message = "One or more users do not exist or are inactive."

    def __init__(self, *, user_ids: list[UUID]):
        super().__init__(
            details={
                "user_ids": user_ids,
            }
        )