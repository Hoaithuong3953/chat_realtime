from typing import Any

class APIResponse:
    """
    Standardized API response format for success and error responses
    """

    @staticmethod
    def success(
        status: str = "success",
        data: Any | None = None,
        *,
        message: str | None = None,
    ):
        if message is None:
            return {
                "status": status,
                "data": data,
            }
        
        return {
            "status": status,
            "message": message,
            "data": data,
        }
    
    @staticmethod
    def error(
        status: str = "error",
        error_code: str | None = None,
        message: str | None = None,
        *,
        details: dict[str, Any] | None = None,
    ):
        if details is None:
            return {
                "status": status,
                "error_code": error_code,
                "message": message,
            }

        return {
            "status": status,
            "error_code": error_code,
            "message": message,
            "details": details,
        }