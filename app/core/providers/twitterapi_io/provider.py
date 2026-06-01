from app.core.exceptions import (
    ErrorCode,
    ProviderRateLimitError,
    ProviderResponseError,
    XAccountNotFoundError,
)
from app.core.providers.base import XProvider
from app.core.providers.twitterapi_io.adapter import TwitterAPIIOAdapter
from app.core.providers.twitterapi_io.client import TwitterAPIIOClient
from app.core.utils import (
    TwitterAPICostCalculator,
    cursor_pagination,
    get_post_ids_from_urls,
    get_usernames_from_urls,
    has_exceeded_max_runtime,
)
from app.schemas import (
    ErrorDTO,
    ProviderRunMetadata,
    XAccountInfo,
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostSearchSorting,
    XPostsResult,
    XProviderKey,
)
from datetime import UTC, datetime
from time import perf_counter
from typing import Any


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

    async def get_accounts_info(self, urls_or_usernames: str) -> XAccountsInfoResult:
        """
        Get normalized account information for multiple usernames.
        Comma-separated usernames and profile URLs are supported.
        """
        started_at = perf_counter()
        normalized = get_usernames_from_urls(urls_or_usernames)
        usernames = [u for u in normalized.split(",") if u]
        results: list = []
        error_code = None
        error_message = None

        for username in usernames:
            try:
                payload = await self.client.get_user_info(username)
                account = self.adapter.to_account_info(payload)
                results.append(account)
            except ProviderRateLimitError as exc:
                if not results:
                    raise
                error_code = ErrorCode.RATE_LIMIT
                error_message = exc.message
                break
            except (ProviderResponseError, XAccountNotFoundError) as exc:
                if error_message is None:
                    error_code = ErrorCode.INVALID_RESPONSE
                    error_message = exc.message
                results.append(ErrorDTO(query=username, exc=exc.message))

        latency_ms = int((perf_counter() - started_at) * 1000)
        returned_count = sum(1 for r in results if isinstance(r, XAccountInfo))

        return XAccountsInfoResult(
            data=results,
            metadata=self._make_metadata(
                input_query=urls_or_usernames,
                latency_ms=latency_ms,
                returned_count=returned_count,
                fetched_at=datetime.now(UTC),
                requested_limit=len(usernames),
                error_code=error_code,
                error_message=error_message,
            ),
        )

    async def search_accounts(
        self,
        query: str,
        limit: int | None,
        max_runtime_sec: int | None = None,
    ) -> XAccountsSearchResult:
        """
        Search accounts by query and return normalized results via adapter.
        """
        started_at = perf_counter()
        accounts = []
        error_code = None
        error_message = None

        async def fetch_page(cursor: str | None) -> dict[str, Any]:
            return await self.client.search_users(query=query, cursor=cursor)

        try:
            async for payload in cursor_pagination(fetch_page):
                accounts.extend(self.adapter.to_accounts_search_results(payload))
                if limit is not None and len(accounts) >= limit:
                    break
                if has_exceeded_max_runtime(started_at, max_runtime_sec):
                    break

        except ProviderRateLimitError as exc:
            if not accounts:
                raise
            error_code = ErrorCode.RATE_LIMIT
            error_message = exc.message

        latency_ms = int((perf_counter() - started_at) * 1000)
        data = accounts[:limit] if limit is not None else accounts

        return XAccountsSearchResult(
            data=data,
            metadata=self._make_metadata(
                input_query=query,
                latency_ms=latency_ms,
                returned_count=len(data),
                fetched_at=datetime.now(UTC),
                requested_limit=limit,
                error_code=error_code,
                error_message=error_message,
            ),
        )

    async def get_account_posts(
        self,
        username_or_userid: str,
        limit: int | None,
        include_replies: bool = False,
    ) -> XPostsResult:
        """
        Get normalized posts from an X account via adapter.
        """
        started_at = perf_counter()
        posts = []
        error_code = None
        error_message = None

        async def fetch_page(cursor: str | None) -> dict[str, Any]:
            return await self.client.get_user_last_tweets(
                username_or_userid=username_or_userid,
                cursor=cursor,
                include_replies=include_replies,
            )

        try:
            async for payload in cursor_pagination(fetch_page):
                posts.extend(self.adapter.to_account_posts(payload))
                if limit is not None and len(posts) >= limit:
                    break

        except ProviderRateLimitError as exc:
            if not posts:
                raise
            error_code = ErrorCode.RATE_LIMIT
            error_message = exc.message

        latency_ms = int((perf_counter() - started_at) * 1000)
        data = posts[:limit] if limit is not None else posts

        return XPostsResult(
            data=data,
            metadata=self._make_metadata(
                input_query=username_or_userid,
                latency_ms=latency_ms,
                returned_count=len(data),
                fetched_at=datetime.now(UTC),
                requested_limit=limit,
                error_code=error_code,
                error_message=error_message,
            ),
        )

    async def search_posts(
        self,
        query: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
        sorting: XPostSearchSorting,
        include_replies: bool = False,
    ) -> XPostsResult:
        """
        Search normalized posts through TwitterAPI.io advanced search.
        """
        started_at = perf_counter()
        posts = []
        error_code = None
        error_message = None
        provider_query = self._build_search_posts_query(
            query, since, until, include_replies
        )

        async def fetch_page(cursor: str | None) -> dict[str, Any]:
            return await self.client.search_tweets(
                query=provider_query,
                query_type=sorting.value,
                cursor=cursor,
            )

        try:
            async for payload in cursor_pagination(fetch_page):
                posts.extend(self.adapter.to_search_posts(payload))
                if limit is not None and len(posts) >= limit:
                    break

        except ProviderRateLimitError as exc:
            if not posts:
                raise
            error_code = ErrorCode.RATE_LIMIT
            error_message = exc.message

        latency_ms = int((perf_counter() - started_at) * 1000)
        data = posts[:limit] if limit is not None else posts

        return XPostsResult(
            data=data,
            metadata=self._make_metadata(
                input_query=provider_query,
                latency_ms=latency_ms,
                returned_count=len(data),
                fetched_at=datetime.now(UTC),
                requested_limit=limit,
                error_code=error_code,
                error_message=error_message,
            ),
        )

    async def get_replies(
        self,
        url_or_id: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
    ) -> XPostsResult:
        """
        Get normalized replies for a specific tweet via adapter.
        """
        started_at = perf_counter()
        tweet_id = get_post_ids_from_urls(url_or_id)
        replies = []
        error_code = None
        error_message = None

        since_unix = int(since.timestamp()) if since is not None else None
        until_unix = int(until.timestamp()) if until is not None else None

        async def fetch_page(cursor: str | None) -> dict[str, Any]:
            return await self.client.get_tweet_replies(
                tweet_id=tweet_id,
                since=since_unix,
                until=until_unix,
                cursor=cursor,
            )

        try:
            async for payload in cursor_pagination(fetch_page):
                replies.extend(self.adapter.to_replies(payload))
                if limit is not None and len(replies) >= limit:
                    break

        except ProviderRateLimitError as exc:
            if not replies:
                raise
            error_code = ErrorCode.RATE_LIMIT
            error_message = exc.message

        latency_ms = int((perf_counter() - started_at) * 1000)
        data = replies[:limit] if limit is not None else replies

        return XPostsResult(
            data=data,
            metadata=self._make_metadata(
                input_query=url_or_id,
                latency_ms=latency_ms,
                returned_count=len(data),
                fetched_at=datetime.now(UTC),
                requested_limit=limit,
                error_code=error_code,
                error_message=error_message,
            ),
        )

    async def get_posts(self, urls_or_ids: str) -> XPostsResult:
        """
        Get normalized posts by URLs or IDs.
        """
        started_at = perf_counter()
        normalized_ids = get_post_ids_from_urls(urls_or_ids)
        payload = await self.client.get_tweets_by_ids(normalized_ids)
        posts = self.adapter.to_posts(payload)
        latency_ms = int((perf_counter() - started_at) * 1000)

        return XPostsResult(
            data=posts,
            metadata=self._make_metadata(
                input_query=urls_or_ids,
                latency_ms=latency_ms,
                returned_count=len(posts),
                fetched_at=datetime.now(UTC),
                requested_limit=None,
            ),
        )

    def _build_search_posts_query(
        self,
        query: str,
        since: datetime | None,
        until: datetime | None,
        include_replies: bool = False,
    ) -> str:
        parts = [query]
        if since is not None:
            parts.append(f"since_time:{int(since.timestamp())}")
        if until is not None:
            parts.append(f"until_time:{int(until.timestamp())}")
        if not include_replies:
            parts.append("-is:reply")
        return " ".join(parts)

    def _make_metadata(
        self,
        input_query: str,
        latency_ms: int,
        returned_count: int,
        fetched_at: datetime,
        requested_limit: int | None = None,
        error_code: ErrorCode | None = None,
        error_message: str | None = None,
    ) -> ProviderRunMetadata:
        """
        Build metadata with estimated cost for any provider response.
        """
        estimated_cost_usd = TwitterAPICostCalculator.calculate(returned_count)
        return ProviderRunMetadata(
            provider_key=XProviderKey.twitterapi_io,
            input_query=input_query,
            latency_ms=latency_ms,
            estimated_cost_usd=estimated_cost_usd,
            requested_limit=requested_limit,
            returned_count=returned_count,
            fetched_at=fetched_at,
            error_code=error_code,
            error_message=error_message,
        )
