from shared.exceptions.common import NotFoundException

class UserNotFoundException(NotFoundException):
    """
    Exception raised when user can not found
    HTTP status code: 404 Not Found
    """
    error_code = "USER_NOT_FOUND"
    message = "User not found."