from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MXCuBE Fault Diagnosis"
    api_prefix: str = "/api"
    database_url: str = "postgresql+asyncpg://mxcube:mxcube@localhost:5432/mxcube"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    log_reader_mode: str = "fixture"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="MXCUBE_")


@lru_cache
def get_settings() -> Settings:
    return Settings()

