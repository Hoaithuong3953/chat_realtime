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
    
    # Handle DRF exceptions
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        app_exc = UnauthorizedException(details=exc.detail)
    
    elif isinstance(exc, PermissionDenied):
        app_exc = ForbiddenException(details=exc.detail)
    
    elif isinstance(exc, ValidationError):
        app_exc = ValidationException(details=exc.detail)
    
    elif isinstance(exc, NotFound):
        app_exc = NotFoundException(details=exc.detail)
    
    else:
        status = getattr(exc, "status_code", None)
        if status is None:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        app_exc = AppException(
            message="An unexpected error occurred.",
            details={},
            http_status=status,
        )

    return Response(
        APIResponse.error(**app_exc.to_dict()),
        status=app_exc.http_status,
    )