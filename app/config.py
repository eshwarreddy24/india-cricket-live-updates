from functools import lru_cache

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    cricket_api_key: str | None = Field(default=None, min_length=1)
    cricket_api_url: HttpUrl = "https://api.cricapi.com/v1/currentMatches"
    cricket_api_timeout_seconds: float = Field(default=8, gt=0, le=60)

    @field_validator("cricket_api_key", mode="before")
    @classmethod
    def blank_key_is_unconfigured(cls, value: str | None) -> str | None:
        if value is None or not str(value).strip():
            return None
        return str(value).strip()

    def validate_provider_configuration(self) -> None:
        if not self.cricket_api_key:
            raise ValueError(
                "CRICKET_API_KEY is not configured. Add a key to .env to load live match data."
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()
