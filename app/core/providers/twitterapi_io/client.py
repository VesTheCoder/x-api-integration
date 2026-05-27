import httpx
from app.core.exceptions import ProviderResponseError
from app.core.http_client import AsyncHTTPClient
from app.core.utils import raise_for_status
from typing import Any


class TwitterAPIIOClient:
    """
    Low-level TwitterAPI.io HTTP client.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        http_client: AsyncHTTPClient,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.http_client = http_client

    async def get_user_info(self, username: str) -> dict[str, Any]:
        """
        Get raw user information by username.
        """
        response = await self.http_client.get(
            f"{self.base_url}/twitter/user/info",
            headers={"X-API-Key": self.api_key},
            params={"userName": username},
        )
        raise_for_status(response)
        payload = self._parse_json(response)
        self._raise_for_semantic_error(payload)
        return payload

    def _parse_json(self, response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderResponseError("Provider returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise ProviderResponseError("Provider returned invalid payload")
        return payload

    def _raise_for_semantic_error(self, payload: dict[str, Any]) -> None:
        if payload.get("status") == "error":
            message = str(
                payload.get("message")
                or payload.get("msg")
                or "Provider returned an error"
            )
            raise ProviderResponseError(message)
