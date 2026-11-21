from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Основные настройки приложения
    app_name: str = "Library Catalog API"
    environment: Literal["development", "staging", "production"]
    debug: bool

    # Настройки базы данных
    database_url: PostgresDsn
    database_pool_size: int = 20

    # Настройки API
    api_v1_prefix: str = "/api/v1"

    # Настройки логирования
    log_level: str = "INFO"

    # Документация FastAPI
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    # Open Library API
    openlibrary_base_url: str = "https://openlibrary.org"
    openlibrary_timeout: float = 10.0

    # Конфигурация загрузки настроек
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
