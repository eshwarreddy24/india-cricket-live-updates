from fastapi.testclient import TestClient

from app.main import app, get_provider, get_settings
from app.provider import ProviderError


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_config_validation_without_api_key(monkeypatch):
    monkeypatch.delenv("CRICKET_API_KEY", raising=False)
    get_settings.cache_clear()

    client = TestClient(app)

    config_response = client.get("/api/config")
    assert config_response.status_code == 200
    assert config_response.json()["configured"] is False

    matches_response = client.get("/api/matches")
    assert matches_response.status_code == 503
    assert matches_response.json()["configured"] is False


class _FailingProvider:
    async def fetch_india_matches(self, team_query: str = "india"):
        raise ProviderError("Cricket provider request timed out")


def test_provider_error_handling(monkeypatch):
    monkeypatch.setenv("CRICKET_API_KEY", "dummy-key")
    get_settings.cache_clear()

    app.dependency_overrides[get_provider] = lambda: _FailingProvider()
    client = TestClient(app)

    response = client.get("/api/matches")

    app.dependency_overrides.clear()

    assert response.status_code == 502
    payload = response.json()
    assert payload["message"] == "Unable to fetch scores from provider right now."
    assert payload["live_matches"] == []
    assert payload["recent_matches"] == []
