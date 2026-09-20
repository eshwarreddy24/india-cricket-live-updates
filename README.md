# India Cricket Live Updates

Simple FastAPI + HTML/CSS/JavaScript app for live and recent India cricket match updates.

## Features
- FastAPI backend with health check and match endpoints
- Frontend with loading, error, and unavailable-data states
- Live and recent India matches from a real provider API
- Configurable API provider settings through environment variables
- Timeout handling and provider error handling
- Backend tests for health, configuration validation, and provider failures

## Provider configuration
This app is wired for [CricAPI](https://www.cricapi.com/). Create a `.env` file from `.env.example` and set your key:

```bash
cp .env.example .env
```

Environment variables:
- `CRICKET_API_PROVIDER` (default: `cricapi`)
- `CRICKET_API_BASE_URL` (default: `https://api.cricapi.com/v1`)
- `CRICKET_API_KEY` (**required** for live data)
- `CRICKET_API_TIMEOUT_SECONDS` (default: `10`)

If `CRICKET_API_KEY` is missing, the app returns an unavailable-data state and does not fabricate scores.

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally
```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## Run tests
```bash
pytest -q
```

## API endpoints
- `GET /health` -> service health
- `GET /api/config` -> provider configuration status
- `GET /api/matches?team=India` -> live + recent matches filtered by team

## Limitations
- Data shape depends on the provider response format.
- Some scorecard details can be unavailable when not returned by the API.
- Free API plans may have request limits.
