# x-api-integration

<p align="center">
  <samp>X Data Gateway</samp>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi&logoColor=white"></a>
  <a href="https://docs.pydantic.dev/"><img src="https://img.shields.io/badge/Pydantic-v2-e92063?style=flat-square&logo=pydantic&logoColor=white"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white"></a>
</p>

<p align="center">
  <b>A plug-in async gateway for X/Twitter data.</b>
  <br>
  Project is ready to operate as a scalable micro-service, where you can add different Twitter(X) data providers according to existing structure. In real use case, allows to query different data providers to achieve API reliability and decrease costs.
  <br>
  One API contract. Normalized DTOs. Per-provider rate limits. Full audit trail.
</p>

<br>

---

```bash
$ curl "http://localhost:8000/accounts?usernames=elonmusk&provider_key=twitterapi_io"
```

```json
{
  "data": [
    {
      "id": "44196397",
      "username": "elonmusk",
      "display_name": "Elon Musk",
      "followers_count": 219000000,
      ...
    }
  ],
  "metadata": {
    "provider_key": "twitterapi_io",
    "latency_ms": 412,
    "returned_count": 1,
    "estimated_cost_usd": 0.00015,
    "fetched_at": "2026-06-18T12:34:56Z"
  }
}
```

<br>

## Why a gateway instead of calling providers directly?

Every X data provider has its own endpoints, request formats, and response shapes. One returns `followersCount`, another `public_metrics.followers_count`. One uses `userId`, another `user_id`.

| Problem | Raw HTTP to each provider API | x-api-integration |
|---|---|---|
| Switch provider | New base URL, new auth, new parsing logic | Change one query param (`?provider_key=`) |
| Add a new source | Build a new client, connect everything again | Implement within 1 interface |
| Data model drift | `public_metrics.followers_count` vs `stats.followerCount` | One `XAccountInfo` schema for every source |
| Response normalization | Manual field mapping per provider | Adapter pattern ready for handling |
| Rate limit burst | Each provider needs its own retry & backoff logic | Per-provider `aiolimiter` + auto-retry |
| Response audit | None | Every provider call has stats and persisted in PostgreSQL |
| Batch lookups | Sequential HTTP calls | Concurrent `asyncio.gather` |
| Cost visibility | Check each provider dashboard separately | `estimated_cost_usd` in every response |

**In short:** you talk to one API. The gateway talks to many.

<br>

## Look once, use immediately

✅ Pass `?provider_key=` to route the same request to different APIs or add routing logic within this micro-service
✅ Add a provider by following existing pattern from abstract class  
✅ All providers return identical `XAccountInfo` / `XPost` schemas  
✅ Every response carries `latency_ms`, `provider_run_id`, and `estimated_cost_usd`  
✅ Partial results survive rate-limit hits — no all-or-nothing failures  
✅ `docker compose up` is persistent for any OS to ease the developement  

<br>

## Quick local start

```bash
# 1. Clone and configure
git clone https://github.com/VesTheCoder/x-api-integration.git
cd x-api-integration
cp .env.sample .env
# Edit .env and set you PROVIDER_X_TWITTERAPI_IO_API_KEY

# 2. Launch
docker compose up

# 3. Query
curl "http://localhost:8000/accounts?usernames=elonmusk&provider_key=twitterapi_io"
```

<br>

## Testing

```bash
# Run all tests
uv run pytest

# Unit tests only
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration
```

| Layer | What's covered | How |
|---|---|---|
| **Unit** | Adapter field mapping, URL normalization, cost calculator | Plain function calls, no I/O |
| **Integration** | HTTP client retry, provider partial-results, service logging, API endpoints, repository persistence | `respx` for HTTP mocks, in-memory SQLite for DB |

<br>

## Architecture at a glance

```
HTTP Request ──→ FastAPI Router ──→ XService ──→ get_provider(provider_key)
                                              │
                                              ↓
                                    ┌─────────┴─────────┐
                                    │   Provider SPI    │
                                    │  (XProvider ABC)  │
                                    └─────────┬─────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
              ┌─────▼─────┐             ┌─────▼─────┐             ┌─────▼─────┐
              │twitterapi │             │ official  │             │  apify    │
              │   _io     │             │ _x API    │             │  scraper  │
              └─────┬─────┘             └─────┬─────┘             └─────┬─────┘
                    │                         │                         │
              Client + Adapter          Client + Adapter          Client + Adapter
                    │                         │                         │
                    └─────────────────────────┴─────────────────────────┘
                                              │
                                              ↓
                                   Normalized DTOs (XAccountInfo / XPost)
                                              │
                                              ↓
                                    PostgreSQL (response_log)
```

**Key design decisions**

| Layer | What it does |
|---|---|
| **Router** | Validates query params; `provider_key` is injected from `XQuery` base model |
| **Service** | `XService` orchestrates provider calls via `@log_provider_call` decorator |
| **Provider SPI** | `XProvider` abstract class with 6 canonical methods; any source must implement it |
| **Client** | Raw HTTP to a specific provider (handles auth, endpoints, pagination cursors) |
| **Adapter** | Converts provider-specific JSON into normalized `XAccountInfo` / `XPost` |
| **Persistence** | Async SQLAlchemy repository logs every request/response snapshot |
| **Rate limiter** | One `aiolimiter` per registered provider, injected at app lifespan |

<br>

## Add a provider in 4 steps

1. Create `app/core/providers/<name>/` with `client.py`, `adapter.py`, `provider.py`
2. Implement `XProvider` and translate raw JSON into `XAccountInfo` / `XPost`
3. Register the key in `XProviderKey`, env prefix in `XProviders`, limiter in `lifespan`
4. Add the provider to the `providers` dict in `get_provider()`

The existing `twitterapi_io` package is the reference implementation (that actually works).

<br>

## Endpoints (provider-agnostic)

| Route | What it does |
|---|---|
| `GET /accounts?usernames=` | Profile info for multiple handles (parallel) |
| `GET /accounts/search?query=` | Account search with cursor pagination |
| `GET /accounts/posts?username_or_userid=` | Latest posts from a user |
| `GET /posts?tweet_ids=` | Posts by ID or URL (batch) |
| `GET /posts/search?query=` | Full-text post search with time filters |
| `GET /posts/replies?url_or_id=` | Reply threads with pagination |

Every endpoint can accept `?provider_key=` to switch the active backend.

<br>

---

<p align="center">
  <a href="https://github.com/VesTheCoder/x-api-integration">GitHub</a>
</p>
