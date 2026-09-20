from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app
from app.provider import ProviderError

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_configuration_rejects_blank_provider_key() -> None:
    settings = Settings(cricket_api_key=" ")
    try:
        settings.validate_provider_configuration()
    except ValueError as exc:
        assert "CRICKET_API_KEY" in str(exc)
    else:
        raise AssertionError("blank key should be rejected")


def test_provider_error_is_user_facing_unavailable_response() -> None:
    with patch("app.main.CricketProvider.fetch_matches", new_callable=AsyncMock) as fetch:
        fetch.side_effect = ProviderError("The cricket data provider could not be reached.")
        response = client.get("/api/matches")
    assert response.status_code == 503
    assert response.json()["unavailable"] is True
    assert "could not be reached" in response.json()["detail"]
