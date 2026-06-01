from app.core.providers.base import XProvider
from app.schemas import (
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostSearchSorting,
    XPostsResult,
)
from datetime import datetime


class XService:
    """
    Application service for X data operations.
    """

    async def get_accounts_info(
        self,
        provider: XProvider,
        urls_or_usernames: str,
    ) -> XAccountsInfoResult:
        """
        Get X account information for multiple usernames.
        """
        return await provider.get_accounts_info(urls_or_usernames)

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

    async def get_posts(
        self,
        provider: XProvider,
        urls_or_ids: str,
    ) -> XPostsResult:
        """
        Get posts by URLs or IDs.
        """
        return await provider.get_posts(urls_or_ids)

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

    async def search_posts(
        self,
        provider: XProvider,
        query: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
        sorting: XPostSearchSorting,
    ) -> XPostsResult:
        """
        Search X posts by query.
        """
        return await provider.search_posts(query, limit, since, until, sorting)
