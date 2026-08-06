from shared.exceptions.base.common import UnauthorizedException

class InvalidRefreshTokenException(UnauthorizedException):
    """
    Exception raised when refresh token is invalid
    HTTP status code: 401 Unauthorized
    """
    error_code = "INVALID_REFRESH_TOKEN"
    message = "Refresh token is invalid."