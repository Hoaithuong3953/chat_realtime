from shared.exceptions.common import ValidationException

class UnsupportedEventException(ValidationException):
    error_code = "UNSUPPORTED_EVENT"
    message = "Unsupported websocket event"

class InvalidPayloadException(ValidationException):
    error_code = "INVALID_PAYLOAD"
    message = "Invalid websocket payload"