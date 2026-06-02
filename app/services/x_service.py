from app.core.providers.base import XProvider
from app.repository.base import AbstractResponseLogRepository
from app.schemas import (
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostSearchSorting,
    XPostsResult,
)
from app.services.response_recorder import log_provider_call
from datetime import datetime


class XService:
    """
    Application service for X data operations.
    Orchestrates provider calls and persists response snapshots in DB.
    """

    def __init__(self, response_repo: AbstractResponseLogRepository) -> None:
        self.response_repo = response_repo

    @log_provider_call
    async def get_accounts_info(
        self,
        provider: XProvider,
        usernames: list[str],
    ) -> XAccountsInfoResult:
        """
        Get X account information for multiple usernames.
        """
        return await provider.get_accounts_info(usernames)

    @log_provider_call
    async def search_accounts(
        self,
        provider: XProvider,
        query: str,
        limit: int | None,
        max_runtime_sec: int | None = None,
    ) -> XAccountsSearchResult:
        """
        Search X accounts by query.
        """
        return await provider.search_accounts(query, limit, max_runtime_sec)

    @log_provider_call
    async def get_account_posts(
        self,
        provider: XProvider,
        username_or_userid: str,
        limit: int | None,
        include_replies: bool = False,
    ) -> XPostsResult:
        """
        Get posts from an X account.
        """
        return await provider.get_account_posts(
            username_or_userid, limit, include_replies
        )

    @log_provider_call
    async def get_posts(
        self,
        provider: XProvider,
        tweet_ids: list[str],
    ) -> XPostsResult:
        """
        Get posts by tweet IDs.
        """
        return await provider.get_posts(tweet_ids)

    @log_provider_call
    async def get_replies(
        self,
        provider: XProvider,
        url_or_id: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
    ) -> XPostsResult:
        """
        Get replies for a specific tweet.
        """
        return await provider.get_replies(url_or_id, limit, since, until)

    @log_provider_call
    async def search_posts(
        self,
        provider: XProvider,
        query: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
        sorting: XPostSearchSorting,
        include_replies: bool = False,
    ) -> XPostsResult:
        """
        Search X posts by query.
        """
        return await provider.search_posts(
            query, limit, since, until, sorting, include_replies
        )
