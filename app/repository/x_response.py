from app.models.x_response import XApiResponse
from app.repository.base import AbstractResponseLogRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class XApiResponseRepository(AbstractResponseLogRepository):
    """
    Implementation of response log repository.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_log(
        self,
        endpoint: str,
        request_params: dict[str, Any],
        response_data: dict[str, Any] | None,
        response_metadata: dict[str, Any] | None,
        error_snapshot: dict[str, Any] | None = None,
    ) -> XApiResponse:
        """
        Persist a single API response log entry.
        """
        model = XApiResponse(
            endpoint=endpoint,
            request_params=request_params,
            response_data=response_data,
            response_metadata=response_metadata,
            error_snapshot=error_snapshot,
        )
        self._session.add(model)
        await self._session.commit()
        return model
