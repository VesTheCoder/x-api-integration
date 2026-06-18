import httpx
import uvicorn
from aiolimiter import AsyncLimiter
from app.api.exception_handlers import provider_exception_handler
from app.api.v1.x.base import router as x_router
from app.core.database.database import close_database, init_database
from app.core.exceptions import ProviderError
from app.schemas import XProviderKey
from app.settings import Settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage database, HTTP client, and per-provider rate limiter lifecycle.
    """
    await init_database(settings.postgres.database_url)
    app.state.http_client = httpx.AsyncClient(timeout=None)
    app.state.provider_limiters = {
        XProviderKey.twitterapi_io: AsyncLimiter(
            settings.providers.twitterapi_io_rate_limit,
            settings.providers.twitterapi_io_rate_limit_period_sec,
        ),
    }
    yield
    await close_database()
    await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(ProviderError, provider_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
    max_age=settings.cors.max_age,
)

app.include_router(x_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
