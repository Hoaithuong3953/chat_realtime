from http import HTTPStatus

from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
    NotFound,
)
from rest_framework.response import Response

from .base import AppException
from .common import (
    UnauthorizedException,
    ValidationException,
    ForbiddenException,
    NotFoundException,
)
from shared.responses import APIResponse

def _build_error_response(
    error_code: str,
    message: str,
    http_status: HTTPStatus,
    details: dict | None = None,
) -> Response:
    """
    Helper function to create a standardized error response using APIResponse

    Args:
        error_code: The error code
        message: The error message
        http_status: The HTTP status code
        details: Additional details about the error

    Returns:
        Response: The standardized error response
    """
    return Response(
        data=APIResponse.error(
            error_code=error_code,
            message=message,
            details=details,
        ),
        status=http_status,
    )

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that returns structured API responses

    Args:
        exc: The exception instance
        context: The context in which the exception occurred
    """
    # Handle custom AppException
    if isinstance(exc, AppException):
        return _build_error_response(
            error_code=exc.error_code,
            message=exc.message,
            http_status=exc.http_status,
            details=exc.details,
        )
    
    # Handle DRF exceptions
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return _build_error_response(
            error_code=UnauthorizedException.error_code,
            message=UnauthorizedException.message,
            http_status=UnauthorizedException.http_status,
            details=exc.detail,
        )
    
    if isinstance(exc, PermissionDenied):
        return _build_error_response(
            error_code=ForbiddenException.error_code,
            message=ForbiddenException.message,
            http_status=ForbiddenException.http_status,
            details=exc.detail,
        )
    
    if isinstance(exc, ValidationError):
        return _build_error_response(
            error_code=ValidationException.error_code,
            message=ValidationException.message,
            http_status=ValidationException.http_status,
            details=exc.detail,
        )
    
    if isinstance(exc, NotFound):
        return _build_error_response(
            error_code=NotFoundException.error_code,
            message=NotFoundException.message,
            http_status=NotFoundException.http_status,
            details=exc.detail,
        )