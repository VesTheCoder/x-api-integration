<p align="center">
  <samp>X Data Gateway</samp>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi&logoColor=white"></a>
  <a href="https://docs.pydantic.dev/"><img src="https://img.shields.io/badge/Pydantic-v2-e92063?style=flat-square&logo=pydantic&logoColor=white"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white"></a>
</p>

# x-api-integration

<p align="center">
  <b>A provider-agnostic FastAPI gateway for X/Twitter data.</b>
  <br>
  Swap data providers without changing a single line of client code.
  <br>
  Rate limits, audit trails, and batch concurrency are built in.
</p>

<br>

---

```bash
$ curl "http://localhost:8000/accounts?usernames=elonmusk" | jq .
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
    "fetched_at": "2026-06-18T12:34:56Z"
  }
}
```

```bash
docker compose up
```

<br>

## Why not call the provider directly?

| Pain point | Raw provider SDK | x-api-integration |
|---|---|---|
| Provider swap | Refactor every call site | Change one env variable |
| Rate limit hit | Manual retry logic | Per-provider limiter + auto-retry |
| Response audit | None | Every call persisted in PostgreSQL |
| Batch lookups | Sequential loops | Concurrent `asyncio.gather` |
| Cost tracking | Spreadsheets | Estimated USD per request in metadata |

<br>

## Look once, use immediately

✅ Pass a full URL or raw ID — URL normalization is automatic  
✅ Change `provider_key` query param to switch backends on the fly  
✅ Every response includes `latency_ms` and `estimated_cost_usd`  
✅ Partial results are returned even when rate limits kick in  
✅ `docker compose up` runs the full stack in 60 seconds  

<br>

## Quick start

```bash
# 1. Clone and configure
git clone https://github.com/VesTheCoder/x-api-integration.git
cd x-api-integration
cp .env.sample .env
# Edit .env and set PROVIDER_X_TWITTERAPI_IO_API_KEY

# 2. Launch
docker compose up

# 3. Query
curl "http://localhost:8000/accounts?usernames=elonmusk"
```

<br>

## Architecture at a glance

```
Client ──→ FastAPI ──→ XService ──→ XProvider (SPI)
                        │   │           │
                        │   │           ↓
                        │   │    HTTP + RateLimiter
                        │   │
                        ↓   ↓
                   PostgreSQL (audit)
```

**Key layers**

| Layer | Role |
|---|---|
| **API** | FastAPI routers with Pydantic query validation and URL normalization |
| **Service** | `XService` orchestrates provider calls and decorates them with `log_provider_call` |
| **Provider (SPI)** | `XProvider` abstract class; current impl: `TwitterAPIIOProvider` via adapter + client |
| **Persistence** | Async SQLAlchemy repository logs every request/response snapshot |
| **Rate limiter** | `aiolimiter` instance per provider, injected at application lifespan |

<br>

## Endpoints

| Route | What it does |
|---|---|
| `GET /accounts?usernames=` | Profile info for multiple handles (parallel) |
| `GET /accounts/search?query=` | Account search with cursor pagination |
| `GET /accounts/posts?username_or_userid=` | Latest posts from a user |
| `GET /posts?tweet_ids=` | Posts by ID or URL (batch) |
| `GET /posts/search?query=` | Full-text post search with time filters |
| `GET /posts/replies?url_or_id=` | Reply threads with pagination |

<br>

---

<p align="center">
  <a href="https://github.com/VesTheCoder/x-api-integration">GitHub</a>
</p>
