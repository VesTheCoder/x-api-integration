from abc import ABC, abstractmethod
from app.models.x_response import XApiResponse
from typing import Any


class AbstractResponseLogRepository(ABC):
    """
    Interface for persisting API response snapshots.
    """

    @abstractmethod
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
