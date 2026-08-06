from shared.exceptions.base.common import ValidationException

class UnsupportedEventException(ValidationException):
    """Exception raised when an unsupported websocket event is encountered"""
    error_code = "UNSUPPORTED_EVENT"
    message = "Unsupported websocket event"

class InvalidPayloadException(ValidationException):
    """Exception raised when the payload of a websocket event is invalid"""
    error_code = "INVALID_PAYLOAD"
    message = "Invalid websocket payload"