from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import Settings, get_settings
from .models import ErrorResponse, MatchesResponse
from .provider import CricketProvider, ProviderError

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="India Cricket Live Updates", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/matches", response_model=MatchesResponse, responses={503: {"model": ErrorResponse}})
async def matches(settings: Settings = Depends(get_settings)) -> MatchesResponse:
    try:
        data = await CricketProvider(settings).fetch_matches()
    except (ProviderError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc), headers={"Cache-Control": "no-store"}) from exc
    return MatchesResponse(matches=data, source="CricAPI")

