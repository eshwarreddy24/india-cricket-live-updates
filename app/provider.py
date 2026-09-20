from typing import Any

import httpx

from .config import Settings
from .models import Match, Score


class ProviderError(RuntimeError):
    """A user-safe error raised when the configured score provider is unavailable."""


class CricketProvider:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def fetch_matches(self) -> list[Match]:
        self.settings.validate_provider_configuration()
        params = {"apikey": self.settings.cricket_api_key, "offset": 0}
        try:
            async with httpx.AsyncClient(timeout=self.settings.cricket_api_timeout_seconds) as client:
                response = await client.get(str(self.settings.cricket_api_url), params=params)
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError("The cricket data provider could not be reached.") from exc

        if not isinstance(payload, dict) or payload.get("status") == "failure":
            raise ProviderError("The cricket data provider returned an invalid response.")
        data = payload.get("data", [])
        if not isinstance(data, list):
            raise ProviderError("The cricket data provider returned an invalid match list.")
        return [self._parse_match(item) for item in data if self._includes_india(item)]

    @staticmethod
    def _includes_india(item: Any) -> bool:
        if not isinstance(item, dict):
            return False
        teams = item.get("teams", [])
        return any("india" in str(team).lower() for team in teams if team)

    @staticmethod
    def _parse_match(item: dict[str, Any]) -> Match:
        scores = []
        for raw_score in item.get("score", []) or []:
            if not isinstance(raw_score, dict):
                continue
            scores.append(
                Score(
                    innings=raw_score.get("inning"),
                    runs=raw_score.get("r"),
                    wickets=raw_score.get("w"),
                    overs=str(raw_score["o"]) if raw_score.get("o") is not None else None,
                )
            )
        teams = [str(team) for team in item.get("teams", []) if team]
        return Match(
            id=str(item.get("id") or item.get("matchId") or item.get("name")),
            name=str(item.get("name") or "India match"),
            match_type=item.get("matchType"),
            status=item.get("status"),
            teams=teams,
            scores=scores,
            venue=(item.get("venue") or {}).get("name") if isinstance(item.get("venue"), dict) else item.get("venue"),
            date=item.get("dateTimeGMT") or item.get("date"),
            scorecard_url=item.get("matchInfo", {}).get("scorecard") if isinstance(item.get("matchInfo"), dict) else None,
        )

