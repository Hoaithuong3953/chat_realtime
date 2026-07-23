from typing import Any

class APIResponse:
    """
    Standardized API response format for success and error responses
    """

    @staticmethod
    def success(
        *,
        status: str = "success",
        data: Any | None = None,
        message: str | None = None,
    ):
        response = {
            "status": status,
        }

        if message is not None:
            response["message"] = message

        if data is not None:
            response["data"] = data
        
        return response
    
    @staticmethod
    def error(
        *,
        status: str = "error",
        error_code: str | None = None,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        response = {
            "status": status,
        }

        if message is not None:
            response["error_code"] = error_code

        if message is not None:
            response["message"] = message

        if details is not None:
            response["details"] = details

        return response