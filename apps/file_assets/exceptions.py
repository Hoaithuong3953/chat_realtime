from shared.exceptions.common import (
    NotFoundException,
    ValidationException,
    PayloadTooLargeException,
)

class FileNotFoundException(NotFoundException):
    """
    Exception raised when the file cannot found
    HTTP status code: 404 Not Found
    """
    error_code = "FILE_NOT_FOUND"
    message = "File is required."

class EmptyFileException(ValidationException):
    """
    Exception raised when the file is empty
    HTTP status code: 400 Bad Request
    """
    error_code = "EMPTY_FILE"
    message = "File is empty."

class InvalidFileExtensionException(ValidationException):
    """
    Exception raised when the file is empty
    HTTP status code: 400 Bad Request
    """
    error_code = "EMPTY_FILE"
    message = "File is empty."

class InvalidContentTypeException(ValidationException):
    """
    Exception raised when the file is empty
    HTTP status code: 400 Bad Request
    """
    error_code = "EMPTY_FILE"
    message = "File is empty."

class FileTooLargeException(PayloadTooLargeException):
    """
    Exception raised when the file size is too large
    HTTP status code: 413 Payload Too Large
    """
    error_code = "FILE_TOO_LARGE"

    def __init__(self, max_file_size: int):
        super().__init__(
            message=f"File size exceeds the maximum allowed size of {max_file_size}."
        )