from typing import Any

from pydantic import BaseModel, Field


class Score(BaseModel):
    innings: str | None = None
    runs: int | None = None
    wickets: int | None = None
    overs: str | None = None


class Match(BaseModel):
    id: str
    name: str
    match_type: str | None = None
    status: str | None = None
    teams: list[str] = Field(default_factory=list)
    scores: list[Score] = Field(default_factory=list)
    venue: str | None = None
    date: str | None = None
    scorecard_url: str | None = None


class MatchesResponse(BaseModel):
    matches: list[Match]
    source: str
    unavailable: bool = False
    message: str | None = None


class ErrorResponse(BaseModel):
    detail: str
    unavailable: bool = True

