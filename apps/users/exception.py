from shared.exceptions.common import ConflictException

class DuplicateUserException(ConflictException):
    """
    Exception raised when trying to register with existing email or username
    HTTP status code: 409 Conflict
    """
    error_code = "DUPLICATE_USER"
    message = "Email or username already exists."

    def __init__(self, field: str):
        super().__init__(details={"field": field})