from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any


async def cursor_pagination(
    fetch_page: Callable[[str | None], Awaitable[dict[str, Any]]],
    page_size: int = 20,
) -> AsyncIterator[dict[str, Any]]:
    """
    Yield cursor-paginated provider pages until the cursor is exhausted.
    """
    cursor: str | None = None
    while True:
        payload = await fetch_page(cursor)
        yield payload
        if not payload.get("has_next_page"):
            return
        cursor = payload.get("next_cursor")
        if not cursor:
            return
        if _page_item_count(payload) < page_size:
            return


def _page_item_count(payload: dict[str, Any]) -> int:
    for value in payload.values():
        if isinstance(value, list):
            return len(value)
        if isinstance(value, dict):
            for inner in value.values():
                if isinstance(inner, list):
                    return len(inner)
    return 0
