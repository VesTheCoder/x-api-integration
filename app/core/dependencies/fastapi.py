import httpx
from aiolimiter import AsyncLimiter
from app.core.database.database import get_db_session
from app.core.http_client import AsyncHTTPClient
from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.core.providers.twitterapi_io.provider import TwitterAPIIOProvider
from app.repository.x_response import XApiResponseRepository
from app.schemas import XProviderKey, XQuery
from app.services.x_service import XService
from app.settings import Settings
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

settings = Settings()


DBSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_x_service(db: DBSession) -> XService:
    """
    Build X data application service with response logging.
    """
    repo = XApiResponseRepository(session=db)
    return XService(response_repo=repo)


def get_provider(request: Request, provider_key: XProviderKey) -> XProvider:
    """
    Get provider by key.
    """
    client = request.app.state.http_client
    limiters: dict[XProviderKey, AsyncLimiter] = request.app.state.provider_limiters
    providers = {
        XProviderKey.twitterapi_io: get_twitterapi_io_provider(
            client, limiters[provider_key]
        ),
    }
    return providers[provider_key]


def get_provider_from_query(
    request: Request,
    params: Annotated[XQuery, Depends()],
) -> XProvider:
    """
    Resolve provider from common X query parameters.
    """
    return get_provider(request, params.provider_key)


def get_twitterapi_io_provider(
    client: httpx.AsyncClient,
    rate_limiter: AsyncLimiter,
) -> TwitterAPIIOProvider:
    """
    Build TwitterAPI.io provider.
    """
    return TwitterAPIIOProvider(
        client=TwitterAPIIOClient(
            base_url=settings.providers.twitterapi_io_base_url,
            api_key=settings.providers.twitterapi_io_api_key,
            http_client=AsyncHTTPClient(client=client, rate_limiter=rate_limiter),
        ),
        adapter=TwitterAPIIOAdapter(),
    )
