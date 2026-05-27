from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.schemas.x_entities import (
    ProviderRunMetadata,
    XAccountInfoResult,
    XProviderKey,
)
from datetime import UTC, datetime
from time import perf_counter


class TwitterAPIIOProvider(XProvider):
    """
    TwitterAPI.io implementation of X provider interface.
    """

    def __init__(
        self,
        client: TwitterAPIIOClient,
        adapter: TwitterAPIIOAdapter,
    ) -> None:
        self.client = client
        self.adapter = adapter

    async def get_account_info(self, username: str) -> XAccountInfoResult:
        """
        Get normalized account information by username.
        """
        started_at = perf_counter()
        payload = await self.client.get_user_info(username)
        account = self.adapter.to_account_info(payload)
        latency_ms = int((perf_counter() - started_at) * 1000)
        return XAccountInfoResult(
            data=account,
            metadata=ProviderRunMetadata(
                provider_key=XProviderKey.twitterapi_io,
                input_query=username,
                estimated_cost=0.00018,
                latency_ms=latency_ms,
                fetched_at=datetime.now(UTC),
            ),
        )
