from app.core.exceptions import ProviderConfigurationError
from app.core.http_client import AsyncHTTPClient
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.core.providers.twitterapi_io.provider import TwitterAPIIOProvider
from app.services.x_service import XService
from app.settings import Settings

settings = Settings()
http_client = AsyncHTTPClient()


def get_twitterapi_io_provider() -> TwitterAPIIOProvider:
    """
    Build TwitterAPI.io provider.
    """
    api_key = settings.providers.twitterapi_io_api_key
    base_url = settings.providers.twitterapi_io_base_url
    if not api_key:
        raise ProviderConfigurationError("TwitterAPI.io API key is not configured")
    if not base_url:
        raise ProviderConfigurationError("TwitterAPI.io base URL is not configured")
    return TwitterAPIIOProvider(
        client=TwitterAPIIOClient(
            base_url=base_url,
            api_key=api_key,
            http_client=http_client,
        ),
        adapter=TwitterAPIIOAdapter(),
    )


def get_x_service() -> XService:
    """
    Build X data application service.
    """
    return XService(provider=get_twitterapi_io_provider())
