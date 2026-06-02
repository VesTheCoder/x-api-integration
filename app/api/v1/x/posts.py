from app.core.dependencies.fastapi import get_provider_from_query, get_x_service
from app.core.providers.base import XProvider
from app.schemas import GetPostsQuery, GetRepliesQuery, SearchPostsQuery, XPostsResult
from app.services.x_service import XService
from fastapi import APIRouter, Depends, Query
from typing import Annotated

router = APIRouter(prefix="/posts", tags=["X posts"])


@router.get("", response_model=XPostsResult)
async def get_posts(
    tweet_ids: Annotated[list[str], Query()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XPostsResult:
    """
    Get X posts by tweet IDs or URLs.
    URLs are accepted and normalized automatically
    (e.g. 987654321, or https://x.com/username/status/123456789).
    """
    params = GetPostsQuery(tweet_ids=tweet_ids)
    return await service.get_posts(
        provider=provider,
        tweet_ids=params.tweet_ids,
    )


@router.get("/search", response_model=XPostsResult)
async def search_posts(
    params: Annotated[SearchPostsQuery, Depends()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XPostsResult:
    """
    Search X posts by query.
    Time filters accept Unix timestamps (e.g. 1748542800) or ISO 8601 / RFC 3339 strings
    (e.g. 2026-05-29T09:40:00.000Z, 2026-05-29T09:40:00+00:00, or 2026-05-29)
    """
    return await service.search_posts(
        provider=provider,
        query=params.query,
        limit=params.limit,
        since=params.since,
        until=params.until,
        sorting=params.sorting,
        include_replies=params.include_replies,
    )


@router.get("/replies", response_model=XPostsResult)
async def get_replies(
    params: Annotated[GetRepliesQuery, Depends()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XPostsResult:
    """
    Get replies for a specific X tweet.
    Time filters accept Unix timestamps (e.g. 1748542800) or ISO 8601 / RFC 3339 strings
    (e.g. 2026-05-29T09:40:00.000Z, 2026-05-29T09:40:00+00:00, or 2026-05-29)
    """
    return await service.get_replies(
        provider=provider,
        url_or_id=params.url_or_id,
        limit=params.limit,
        since=params.since,
        until=params.until,
    )
