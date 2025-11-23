# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Manager API"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    """
    Cache settings so we don't reload .env file on every request
    """
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
