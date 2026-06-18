import functools
import inspect
from app.repository.base import AbstractResponseLogRepository
from app.schemas import (
    XAccountsInfoResult,
    XAccountsSearchResult,
    XPostsResult,
)
from pydantic_core import to_jsonable_python
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


async def record(
    repo: AbstractResponseLogRepository,
    endpoint: str,
    request_params: dict[str, Any],
    result: (XAccountsInfoResult | XAccountsSearchResult | XPostsResult | None) = None,
    exc: Exception | None = None,
) -> None:
    """
    Persist a provider response or error snapshot.
    """
    await repo.create_log(
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


def log_provider_call(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[T]]:
    """
    Decorator that wraps a provider call and persists its snapshot.
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
            await record(service.response_repo, endpoint, params, result=result)
            return result
        except Exception as exc:
            await record(service.response_repo, endpoint, params, exc=exc)
            raise

    return wrapper
