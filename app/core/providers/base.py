from abc import ABC, abstractmethod
from app.schemas import XAccountInfoResult, XAccountPostsResult, XAccountsSearchResult


class XProvider(ABC):
    """
    Base interface for X data providers.
    """

    @abstractmethod
    async def get_account_info(self, username: str) -> XAccountInfoResult:
        """
        Get normalized X account information.
        """

    @abstractmethod
    async def search_accounts(
        self,
        query: str,
        limit: int,
        max_runtime_sec: int | None = None,
    ) -> XAccountsSearchResult:
        """
        Search for normalized X accounts.
        """

    @abstractmethod
    async def get_account_posts(
        self,
        username_or_userid: str,
        limit: int,
        include_replies: bool = False,
    ) -> XAccountPostsResult:
        """
        Get normalized posts from an X account.
        """
