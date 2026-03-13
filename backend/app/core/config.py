from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Resume Analyzer & Job Matcher"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/resume_matcher"
    cors_origins: str = "http://localhost:5173"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    max_upload_size_mb: int = 5

    def parsed_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
