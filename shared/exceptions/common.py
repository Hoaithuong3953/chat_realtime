from http import HTTPStatus
from .base import AppException

class ValidationException(AppException):
    """
    Exception raised when validation of input data fails
    HTTP status code: 400 Bad Request
    """
    error_code = "VALIDATION_ERROR"
    message = "Validation failed for the provided data."
    http_status = HTTPStatus.BAD_REQUEST

class UnauthorizedException(AppException):
    """
    Exception raised when a user is not authorized to access a resource
    HTTP status code: 401 Unauthorized
    """
    error_code = "UNAUTHORIZED"
    message = "Authentication is required."
    http_status = HTTPStatus.UNAUTHORIZED

class ForbiddenException(AppException):
    """
    Exception raised when a user is authenticated but does not have permission
    HTTP status code: 403 Forbidden
    """
    error_code = "FORBIDDEN"
    message = "Permission denied."
    http_status = HTTPStatus.FORBIDDEN

class NotFoundException(AppException):
    """
    Exception raised when a requested resource is not found
    HTTP status code: 404 Not Found
    """
    error_code = "NOT_FOUND"
    message = "The requested resource was not found."
    http_status = HTTPStatus.NOT_FOUND

class ConflictException(AppException):
    """
    Exception raised when a request cannot be completed due to a conflict with the current state of the resource
    HTTP status code: 409 Conflict
    """
    error_code = "CONFLICT"
    message = "Conflict occurred with the current state of the resource."
    http_status = HTTPStatus.CONFLICT

class RateLimitException(AppException):
    """
    Exception raised when a user exceeds the allowed number of requests in a given time frame
    HTTP status code: 429 Too Many Requests
    """
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "Rate limit exceeded. Please try again later."
    http_status = HTTPStatus.TOO_MANY_REQUESTS

class InternalServerException(AppException):
    """
    Exception raised when an unexpected server error occurs
    HTTP status code: 500 Internal Server Error
    """
    error_code = "INTERNAL_SERVER_ERROR"
    message = "Internal server error."
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR