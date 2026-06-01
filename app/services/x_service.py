import functools
import inspect
from app.core.providers.base import XProvider
from app.repository.base import AbstractResponseLogRepository
from app.schemas import (
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostSearchSorting,
    XPostsResult,
)
from datetime import datetime
from pydantic_core import to_jsonable_python
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def _log_provider_call(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[T]]:
    """
    Decorator that wraps a provider call with response logging.
    """
    sig = inspect.signature(func)

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        service = bound.arguments["self"]
        endpoint = func.__name__
        params = to_jsonable_python(
            {
                name: value
                for name, value in bound.arguments.items()
                if name not in ("self", "provider")
            }
        )

        try:
            result = await func(*args, **kwargs)
            await service._save_log(endpoint, params, result=result)
            return result
        except Exception as exc:
            await service._save_log(endpoint, params, exc=exc)
            raise

    return wrapper


class XService:
    """
    Application service for X data operations.
    Orchestrates provider calls and persists response snapshots in DB.
    """

    def __init__(self, response_repo: AbstractResponseLogRepository) -> None:
        self._response_repo = response_repo

    @_log_provider_call
    async def get_accounts_info(
        self,
        provider: XProvider,
        urls_or_usernames: str,
    ) -> XAccountsInfoResult:
        """
        Get X account information for multiple usernames.
        """
        return await provider.get_accounts_info(urls_or_usernames)

    @_log_provider_call
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

    @_log_provider_call
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

    @_log_provider_call
    async def get_posts(
        self,
        provider: XProvider,
        urls_or_ids: str,
    ) -> XPostsResult:
        """
        Get posts by URLs or IDs.
        """
        return await provider.get_posts(urls_or_ids)

    @_log_provider_call
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

    @_log_provider_call
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

    async def _save_log(
        self,
        endpoint: str,
        request_params: dict[str, Any],
        result: (
            XAccountsInfoResult | XAccountsSearchResult | XPostsResult | None
        ) = None,
        exc: Exception | None = None,
    ) -> None:
        """
        Persist a provider response or error snapshot.
        """

        await self._response_repo.create_log(
            endpoint=endpoint,
            request_params=request_params,
            response_data=result.model_dump(mode="json") if result else None,
            response_metadata=(
                result.metadata.model_dump(mode="json")
                if result and result.metadata
                else None
            ),
            error_snapshot=(
                {
                    "error_code": getattr(exc, "error_code", None),
                    "error_message": getattr(exc, "message", str(exc)),
                }
                if exc
                else None
            ),
        )
