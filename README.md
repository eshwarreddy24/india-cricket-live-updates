# India Cricket Live Updates

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://github.com/eshwarreddy24/india-cricket-live-updates/actions/workflows/tests.yml/badge.svg)](https://github.com/eshwarreddy24/india-cricket-live-updates/actions/workflows/tests.yml)
[![GitHub stars](https://img.shields.io/github/stars/eshwarreddy24/india-cricket-live-updates?style=flat)](https://github.com/eshwarreddy24/india-cricket-live-updates/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/eshwarreddy24/india-cricket-live-updates?style=flat)](https://github.com/eshwarreddy24/india-cricket-live-updates/network/members)
[![GitHub issues](https://img.shields.io/github/issues/eshwarreddy24/india-cricket-live-updates)](https://github.com/eshwarreddy24/india-cricket-live-updates/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/eshwarreddy24/india-cricket-live-updates)](https://github.com/eshwarreddy24/india-cricket-live-updates/pulls)
[![Last commit](https://img.shields.io/github/last-commit/eshwarreddy24/india-cricket-live-updates)](https://github.com/eshwarreddy24/india-cricket-live-updates/commits/main)
[![Repo size](https://img.shields.io/github/repo-size/eshwarreddy24/india-cricket-live-updates)](https://github.com/eshwarreddy24/india-cricket-live-updates)

A small FastAPI application with a beginner-friendly HTML/CSS/JavaScript frontend for live and recent cricket matches involving India. The application displays only data returned by a configured cricket data provider: it never ships with fabricated or fallback scores.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Copy `.env.example` to `.env` and set `CRICKET_API_KEY` to a valid key from [CricAPI / CricketData.org](https://cricketdata.org/).

## Run locally

```bash
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Use **Refresh scores** to request the latest provider data; if a later request fails, the app keeps the last successful scores visible and labels when they were updated. The JSON API is available at `/api/matches`, and `/health` provides a basic health check.

## Provider configuration

The default endpoint is CricAPI's `currentMatches` endpoint:

| Variable | Required | Description |
| --- | --- | --- |
| `CRICKET_API_KEY` | Yes | Provider API key; keep it in `.env` or the deployment secret store. |
| `CRICKET_API_URL` | No | HTTPS provider endpoint, defaulting to CricAPI `currentMatches`. |
| `CRICKET_API_TIMEOUT_SECONDS` | No | Request timeout from 0 to 60 seconds, defaulting to 8. |

The provider response is filtered to matches whose team list contains India and mapped into a small stable API model. Provider timeouts, HTTP failures, malformed responses, and missing configuration are reported as an unavailable-data state (HTTP 503); the frontend shows that message rather than inventing scores.

## Test

```bash
pytest
```

Tests cover the health endpoint, provider configuration validation, and user-facing provider failure handling.

## Limitations and data-source notes

- Coverage, refresh frequency, quotas, and scorecard fields depend on the configured CricAPI plan and upstream provider.
- This application does not persist scores, calculate results, or replace an official scorecard.
- Scorecard details are shown only when the provider includes them. The app does not infer missing innings, runs, wickets, or overs.
- An API key is intentionally not included in this repository. Never commit `.env` or provider credentials.

The existing project is distributed under the MIT License; see `LICENSE`.
