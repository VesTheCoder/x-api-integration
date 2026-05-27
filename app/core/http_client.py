import httpx
from app.core.exceptions import ProviderUnavailableError
from typing import Any


class AsyncHTTPClient:
    """
    Reusable asynchronous HTTP client wrapper.
    """

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Execute an asynchronous GET request.
        """
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                return await client.get(url, headers=headers, params=params)
        except httpx.RequestError as exc:
            raise ProviderUnavailableError(str(exc)) from exc
