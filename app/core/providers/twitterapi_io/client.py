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

    async def search_users(
        self,
        query: str,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """
        Search raw users by query with optional pagination.
        """
        params = {"query": query}
        if cursor is not None:
            params["cursor"] = cursor
        response = await self.http_client.get(
            f"{self.base_url}/twitter/user/search",
            headers={"X-API-Key": self.api_key},
            params=params,
        )
        raise_for_status(response)
        payload = self._parse_json(response)
        self._raise_for_semantic_error(payload)
        return payload

    async def get_user_last_tweets(
        self,
        username_or_userid: str,
        cursor: str | None = None,
        include_replies: bool = False,
    ) -> dict[str, Any]:
        """
        Get raw latest tweets by user ID or username with optional pagination.
        """
        params: dict[str, Any] = {}
        if username_or_userid.isdigit():
            params["userId"] = username_or_userid
        else:
            params["userName"] = username_or_userid
        if cursor is not None:
            params["cursor"] = cursor
        if include_replies:
            params["includeReplies"] = "true"
        response = await self.http_client.get(
            f"{self.base_url}/twitter/user/last_tweets",
            headers={"X-API-Key": self.api_key},
            params=params,
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
