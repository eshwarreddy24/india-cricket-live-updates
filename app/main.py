from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, load_settings
from app.provider import CricketApiProvider, ProviderError

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="India Cricket Live Updates", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@lru_cache
def get_settings() -> Settings:
    return load_settings()


def get_provider(settings: Settings = Depends(get_settings)) -> CricketApiProvider:
    return CricketApiProvider(settings)


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config")
def config(settings: Settings = Depends(get_settings)) -> dict[str, str | bool]:
    if settings.is_configured:
        return {
            "configured": True,
            "provider": settings.provider,
            "message": "Provider is configured and ready.",
        }

    return {
        "configured": False,
        "provider": settings.provider,
        "message": "API key is missing. Set CRICKET_API_KEY to load live data.",
    }


@app.get("/api/matches")
async def matches(
    team: str = Query(default="India", min_length=2, max_length=30, pattern=r"^[A-Za-z ]+$"),
    settings: Settings = Depends(get_settings),
    provider: CricketApiProvider = Depends(get_provider),
):
    if not settings.is_configured:
        return JSONResponse(
            status_code=503,
            content={
                "configured": False,
                "message": "Live data unavailable: provider is not configured.",
                "live_matches": [],
                "recent_matches": [],
            },
        )

    try:
        data = await provider.fetch_india_matches(team_query=team.lower())
    except ProviderError as exc:
        return JSONResponse(
            status_code=502,
            content={
                "configured": True,
                "message": str(exc),
                "live_matches": [],
                "recent_matches": [],
            },
        )

    data["configured"] = True
    return data
