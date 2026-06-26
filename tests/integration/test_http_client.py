import httpx
import pytest
import respx
from app.core.exceptions import ProviderUnavailableError
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestAsyncHTTPClient:
    """
    Tests for AsyncHTTPClient retry and rate-limit behavior.
    """

    @respx.mock
    async def test_retries_on_429_then_succeeds(self, http_client):
        route = respx.get("https://example.com/api").mock(
            side_effect=[
                httpx.Response(429),
                httpx.Response(200, json={"ok": True}),
            ]
        )
        with patch("app.core.http_client.asyncio.sleep", new=AsyncMock()):
            response = await http_client.get("https://example.com/api")

        assert response.status_code == 200
        assert route.call_count == 2

    @respx.mock
    async def test_raises_unavailable_on_request_error(self, http_client):
        respx.get("https://example.com/api").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ProviderUnavailableError, match="Connection refused"):
            await http_client.get("https://example.com/api")

    @respx.mock
    async def test_raises_unavailable_after_max_retries(self, http_client):
        respx.get("https://example.com/api").mock(return_value=httpx.Response(429))
        with patch("app.core.http_client.asyncio.sleep", new=AsyncMock()):
            with pytest.raises(ProviderUnavailableError):
                await http_client.get("https://example.com/api")
