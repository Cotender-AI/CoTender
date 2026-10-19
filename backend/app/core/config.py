from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All runtime configuration comes from environment variables (see .env.example)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://inteltps:inteltps@localhost:5432/inteltps"

    jwt_secret: str = "change-me"
    access_token_minutes: int = 30
    refresh_token_days: int = 7

    azure_storage_connection_string: str = ""
    blob_container: str = "tender-documents"
    queue_name: str = "extraction-jobs"

    cors_origins: list[str] = ["http://localhost:3000"]

    max_upload_mb: int = 20
    max_pages: int = 50


@lru_cache
def get_settings() -> Settings:
    return Settings()
