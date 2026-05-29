import asyncio
import httpx
from app.core.exceptions import ProviderUnavailableError
from typing import Any

REQUEST_DELAY_MS = 300
MAX_RETRIES = 3


class AsyncHTTPClient:
    """
    Reusable asynchronous HTTP client wrapper.
    """

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Execute an asynchronous GET request with retry on 429.
        """
        for attempt in range(MAX_RETRIES):
            try:
                response = await self.client.get(url, headers=headers, params=params)
                if response.status_code == 429:
                    if attempt < MAX_RETRIES - 1:
                        delay = REQUEST_DELAY_MS / 1000 * (2**attempt)
                        await asyncio.sleep(delay)
                        continue
                return response
            except httpx.RequestError as exc:
                raise ProviderUnavailableError(str(exc)) from exc
        raise ProviderUnavailableError()
