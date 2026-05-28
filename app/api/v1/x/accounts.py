from app.core.dependencies.fastapi import get_provider_from_query, get_x_service
from app.core.providers.base import XProvider
from app.schemas.x_entities import XAccountInfoResult, XAccountsSearchResult
from app.schemas.x_queries import GetAccountInfoQuery, SearchAccountsQuery
from app.services.x_service import XService
from fastapi import APIRouter, Depends
from typing import Annotated

router = APIRouter(prefix="/accounts", tags=["X accounts"])


@router.get("/search", response_model=XAccountsSearchResult)
async def search_accounts(
    params: Annotated[SearchAccountsQuery, Depends()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XAccountsSearchResult:
    """
    Search X accounts by query.
    """
    return await service.search_accounts(
        provider=provider,
        query=params.query,
        limit=params.limit,
        max_runtime_sec=params.max_runtime_sec,
    )


@router.get("/{username}", response_model=XAccountInfoResult)
async def get_account_info(
    username: str,
    params: Annotated[GetAccountInfoQuery, Depends()],
    service: Annotated[XService, Depends(get_x_service)],
    provider: Annotated[XProvider, Depends(get_provider_from_query)],
) -> XAccountInfoResult:
    """
    Router function.
    Get X account information by username.
    """
    return await service.get_account_info(provider, username)
