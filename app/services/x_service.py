from app.core.providers.base import XProvider
from app.schemas import XAccountInfoResult, XAccountsSearchResult, XPostsResult


class XService:
    """
    Application service for X data operations.
    """

    async def get_account_info(
        self,
        provider: XProvider,
        username: str,
    ) -> XAccountInfoResult:
        """
        Get X account information by username.
        """
        return await provider.get_account_info(username)

    async def search_accounts(
        self,
        provider: XProvider,
        query: str,
        limit: int,
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
        limit: int,
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
