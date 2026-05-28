from app.core.exceptions import ErrorCode, ProviderRateLimitError
from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.core.utils import has_exceeded_max_runtime
from app.schemas import (
    ProviderRunMetadata,
    XAccountInfoResult,
    XAccountsSearchMetadata,
    XAccountsSearchResult,
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
                latency_ms=latency_ms,
                fetched_at=datetime.now(UTC),
            ),
        )

    async def search_accounts(
        self,
        query: str,
        limit: int,
        max_runtime_sec: int | None = None,
    ) -> XAccountsSearchResult:
        """
        Search accounts by query and return normalized results via adapter.
        """
        started_at = perf_counter()
        cursor: str | None = None
        accounts = []
        error_code = None
        error_message = None

        while len(accounts) < limit:
            try:
                payload = await self.client.search_users(query=query, cursor=cursor)
                accounts.extend(self.adapter.to_accounts_search_results(payload))
                if len(accounts) >= limit:
                    break
                if not payload.get("has_next_page"):
                    break
                cursor = payload.get("next_cursor")
                if not cursor:
                    break
                if has_exceeded_max_runtime(started_at, max_runtime_sec):
                    break
            except ProviderRateLimitError:
                if not accounts:
                    raise
                error_code = ErrorCode.RATE_LIMIT
                error_message = "Provider rate limit reached"
                break

        latency_ms = int((perf_counter() - started_at) * 1000)
        data = accounts[:limit]
        return XAccountsSearchResult(
            data=data,
            metadata=XAccountsSearchMetadata(
                provider_key=XProviderKey.twitterapi_io,
                input_query=query,
                latency_ms=latency_ms,
                fetched_at=datetime.now(UTC),
                requested_limit=limit,
                returned_count=len(data),
                error_code=error_code,
                error_message=error_message,
            ),
        )
