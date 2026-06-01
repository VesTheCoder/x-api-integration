from abc import ABC, abstractmethod
from app.schemas import (
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostSearchSorting,
    XPostsResult,
)
from datetime import datetime


class XProvider(ABC):
    """
    Base interface for X data providers.
    """

    @abstractmethod
    async def get_accounts_info(self, urls_or_usernames: str) -> XAccountsInfoResult:
        """
        Get normalized X account information for multiple usernames.
        """

    @abstractmethod
    async def search_accounts(
        self,
        query: str,
        limit: int | None,
        max_runtime_sec: int | None = None,
    ) -> XAccountsSearchResult:
        """
        Search for normalized X accounts.
        """

    @abstractmethod
    async def get_account_posts(
        self,
        username_or_userid: str,
        limit: int | None,
        include_replies: bool = False,
    ) -> XPostsResult:
        """
        Get normalized posts from an X account.
        """

    @abstractmethod
    async def get_posts(self, urls_or_ids: str) -> XPostsResult:
        """
        Get normalized posts by URLs or IDs.
        """

    @abstractmethod
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
        Search for normalized X posts.
        """

    @abstractmethod
    async def get_replies(
        self,
        url_or_id: str,
        limit: int | None,
        since: datetime | None,
        until: datetime | None,
    ) -> XPostsResult:
        """
        Get normalized replies for a specific tweet.
        """
