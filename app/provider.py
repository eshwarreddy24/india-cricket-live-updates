from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings


class ProviderError(Exception):
    pass


class CricketApiProvider:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch_india_matches(self, team_query: str = "india") -> dict[str, Any]:
        if not self.settings.is_configured:
            raise ProviderError("Cricket API is not configured")

        params = {"apikey": self.settings.api_key, "offset": 0}
        timeout = httpx.Timeout(self.settings.timeout_seconds)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                live_response = await client.get(f"{self.settings.api_base_url}/currentMatches", params=params)
                live_response.raise_for_status()

                recent_response = await client.get(f"{self.settings.api_base_url}/matches", params=params)
                recent_response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ProviderError("Cricket provider request timed out") from exc
        except httpx.HTTPError as exc:
            raise ProviderError("Cricket provider request failed") from exc

        live_data = live_response.json().get("data", [])
        recent_data = recent_response.json().get("data", [])

        return {
            "provider": self.settings.provider,
            "team": "India",
            "live_matches": self._filter_and_normalize(live_data, team_query),
            "recent_matches": self._filter_and_normalize(recent_data, team_query),
        }

    def _filter_and_normalize(self, matches: list[dict[str, Any]], team_query: str) -> list[dict[str, Any]]:
        query = team_query.lower()
        result = []

        for match in matches:
            name = str(match.get("name", ""))
            teams = [str(team) for team in match.get("teams", [])]
            team_text = " ".join(teams).lower()

            if query not in name.lower() and query not in team_text:
                continue

            innings = []
            for inning in match.get("score", []) or []:
                innings.append(
                    {
                        "inning": inning.get("inning") or "Unknown innings",
                        "runs": inning.get("r"),
                        "wickets": inning.get("w"),
                        "overs": inning.get("o"),
                    }
                )

            result.append(
                {
                    "id": match.get("id"),
                    "name": name or "Match name unavailable",
                    "teams": teams,
                    "status": match.get("status") or "Status unavailable",
                    "match_type": match.get("matchType") or "Unknown",
                    "venue": match.get("venue") or "Venue unavailable",
                    "date": match.get("date") or "Date unavailable",
                    "innings": innings,
                }
            )

        return result
