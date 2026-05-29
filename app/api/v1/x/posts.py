from app.core.dependencies.fastapi import get_provider_from_query, get_x_service
from app.core.providers.base import XProvider
from app.schemas import GetPostsQuery, XPostsResult
from app.services.x_service import XService
from fastapi import APIRouter, Depends
from typing import Annotated

router = APIRouter(prefix="/posts", tags=["X posts"])


@router.get("", response_model=XPostsResult)
async def get_posts(
    params: Annotated[GetPostsQuery, Depends()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XPostsResult:
    """
    Get X posts by tweet IDs or URLs.
    """
    return await service.get_posts(
        provider=provider,
        urls_or_ids=params.urls_or_ids,
    )
