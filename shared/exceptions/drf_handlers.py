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
from shared.logging import get_logger

logger = get_logger(__name__)

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
        request = context.get("request")
        view = context.get("view")
        logger.exception(
            "Unhandled exception. view=%s method=%s path=%s",
            view.__class__.__name__ if view else "unknown",
            request.method if request else "?",
            request.path if request else "?",
            exc_info=exc,
        )
        app_exc = AppException(
            message="An unexpected error occurred.",
            details={},
        )

    return Response(
        APIResponse.error(**app_exc.to_dict()),
        status=app_exc.http_status,
    )