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

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that returns structured API responses

    Args:
        exc: The exception instance
        context: The context in which the exception occurred
    """
    if isinstance(exc, AppException):
        app_exc = exc

    # Handle DRF exceptions
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        app_exc = UnauthorizedException(details=exc.detail)
    
    elif isinstance(exc, PermissionDenied):
        app_exc = ForbiddenException(details=exc.detail)
    
    elif isinstance(exc, ValidationError):
        app_exc = ValidationException(details=exc.detail)
    
    elif isinstance(exc, NotFound):
        app_exc = NotFoundException(details=exc.detail)
    
    else:
        app_exc = AppException(
            message="An unexpected error occurred.",
            details={},
        )

    return Response(
        APIResponse.error(**app_exc.to_dict()),
        status=app_exc.http_status,
    )