import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str
    api_base_url: str
    api_key: str
    timeout_seconds: float

    @property
    def is_configured(self) -> bool:
        return bool(self.api_base_url and self.api_key)


def load_settings() -> Settings:
    provider = os.getenv("CRICKET_API_PROVIDER", "cricapi").strip() or "cricapi"
    api_base_url = os.getenv("CRICKET_API_BASE_URL", "https://api.cricapi.com/v1").strip()
    api_key = os.getenv("CRICKET_API_KEY", "").strip()

    raw_timeout = os.getenv("CRICKET_API_TIMEOUT_SECONDS", "10").strip()
    timeout_seconds = 10.0
    try:
        parsed_timeout = float(raw_timeout)
        if 1 <= parsed_timeout <= 60:
            timeout_seconds = parsed_timeout
    except ValueError:
        timeout_seconds = 10.0

    return Settings(
        provider=provider,
        api_base_url=api_base_url,
        api_key=api_key,
        timeout_seconds=timeout_seconds,
    )
