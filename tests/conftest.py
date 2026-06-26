import os

os.environ["PROVIDER_X_TWITTERAPI_IO_API_KEY"] = "test-key"
os.environ["PROVIDER_X_TWITTERAPI_IO_BASE_URL"] = "https://test.twitterapi.io"
os.environ["PROVIDER_X_TWITTERAPI_IO_RATE_LIMIT"] = "18"
os.environ["PROVIDER_X_TWITTERAPI_IO_RATE_LIMIT_PERIOD_SEC"] = "1"

import httpx
import pytest
import pytest_asyncio
from aiolimiter import AsyncLimiter
from app.core.database.base import Base
from app.core.dependencies.fastapi import get_provider_from_query, get_x_service
from app.core.http_client import AsyncHTTPClient
from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.main import app
from app.repository.base import AbstractResponseLogRepository
from app.repository.x_response import XApiResponseRepository
from app.services.x_service import XService
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from unittest.mock import AsyncMock


@pytest.fixture
def adapter():
    """
    TwitterAPIIOAdapter instance for adapter tests.
    """
    return TwitterAPIIOAdapter()


@pytest.fixture
def http_client():
    """
    AsyncHTTPClient with real httpx.AsyncClient and permissive rate limiter.
    """
    return AsyncHTTPClient(
        client=httpx.AsyncClient(),
        rate_limiter=AsyncLimiter(100, 1),
    )


@pytest.fixture
def twitter_client(http_client):
    """
    TwitterAPIIOClient wired to the test http_client.
    """
    return TwitterAPIIOClient(
        base_url="https://test.twitterapi.io",
        api_key="test-key",
        http_client=http_client,
    )


@pytest.fixture
def mock_provider():
    """
    AsyncMock implementing the XProvider interface.
    """
    return AsyncMock(spec=XProvider)


@pytest.fixture
def mock_repo():
    """
    AsyncMock implementing the AbstractResponseLogRepository interface.
    """
    return AsyncMock(spec=AbstractResponseLogRepository)


@pytest.fixture
def service(mock_repo):
    """
    XService with a mocked response repository.
    """
    return XService(response_repo=mock_repo)


@pytest.fixture
def mock_service():
    """
    AsyncMock for XService used in API endpoint tests.
    """
    return AsyncMock()


@pytest_asyncio.fixture
async def db_engine():
    """
    In-memory SQLite async engine with all tables created.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    """
    Async session from the in-memory SQLite engine.
    """
    session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest.fixture
def db_repo(db_session):
    """
    Real XApiResponseRepository backed by in-memory SQLite.
    """
    return XApiResponseRepository(session=db_session)


@pytest_asyncio.fixture
async def client(mock_service, mock_provider):
    """
    Async HTTP client wired to the FastAPI ASGI app with mocked dependencies.
    """
    app.dependency_overrides[get_x_service] = lambda: mock_service
    app.dependency_overrides[get_provider_from_query] = lambda: mock_provider

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
