from app.core.http_client import AsyncHTTPClient
from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.core.providers.twitterapi_io.provider import TwitterAPIIOProvider
from app.schemas import XProviderKey, XQuery
from app.services.x_service import XService
from app.settings import Settings
from fastapi import Depends
from typing import Annotated

settings = Settings()
http_client = AsyncHTTPClient()


def get_x_service() -> XService:
    """
    Build X data application service.
    """
    return XService()


def get_provider(provider_key: XProviderKey) -> XProvider:
    """
    Get provider by key.
    """
    providers = {
        XProviderKey.twitterapi_io: get_twitterapi_io_provider(),
    }
    return providers[provider_key]


def get_provider_from_query(params: Annotated[XQuery, Depends()]) -> XProvider:
    """
    Resolve provider from common X query parameters.
    """
    return get_provider(params.provider_key)


def get_twitterapi_io_provider() -> TwitterAPIIOProvider:
    """
    Build TwitterAPI.io provider.
    """
    return TwitterAPIIOProvider(
        client=TwitterAPIIOClient(
            base_url=settings.providers.twitterapi_io_base_url,
            api_key=settings.providers.twitterapi_io_api_key,
            http_client=http_client,
        ),
        adapter=TwitterAPIIOAdapter(),
    )
