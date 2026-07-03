from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    """
    Application configuration loaded from evironment variables (.env)
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Django settings
    SECRET_KEY: str = Field(
        ...,
        description="Django secret key (required)"
    )
    DEBUG: bool = Field(
        default=True,
        description="Debug mode (default True)"
        )
    ALLOWED_HOSTS: list[str] = Field(
        default=[],
        description="Allowed hosts (default empty list)"
    )

    # Database configuration (required)
    DB_NAME: str = Field(..., description="Database name (required)")
    DB_USER: str = Field(..., description="Database user (required)")
    DB_PASSWORD: str = Field(..., description="Database password (required)")
    DB_HOST: str = Field(..., description="Database host (required)")
    DB_PORT: int = Field(..., description="Database port (required)")

    # CORS configuration
    CORS_ALLOWED_ORIGINS: list[str] = Field(
        default=[],
        description="CORS allowed origins (default empty list)"
    )

    # JWT configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Access token expiration time in minutes (default 15 minutes)"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days (default 7 days)"
    )

    # Logging configuration
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level (default INFO)",
    )
    LOG_FORMAT: str = Field(
        default="{asctime} | {levelname} | {name} | {message}",
        description="Logging format (can be overridden by LOG_FORMAT in .env)"
    )
    LOG_DATE_FORMAT: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Logging date format (can be overridden by LOG_DATE_FORMAT in .env)"
    )

settings = Settings()