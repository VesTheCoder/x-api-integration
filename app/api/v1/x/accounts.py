from app.core.dependencies.fastapi import get_x_service
from app.schemas.x_entities import XAccountInfoResult
from app.services.x_service import XService
from fastapi import APIRouter, Depends
from typing import Annotated

router = APIRouter(prefix="/accounts", tags=["X accounts"])


@router.get("/{username}", response_model=XAccountInfoResult)
async def get_account_info(
    username: str,
    service: Annotated[XService, Depends(get_x_service)],
) -> XAccountInfoResult:
    """
    Router function.
    Get X account information by username.
    """
    return await service.get_account_info(username)
