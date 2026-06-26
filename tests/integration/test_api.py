import pytest
from app.core.exceptions import ProviderRateLimitError
from tests.factories import accounts_info_result_factory
from unittest.mock import AsyncMock


@pytest.mark.integration
class TestAccountsEndpoint:
    """
    Tests for GET /api/v1/x/accounts endpoint.
    """

    async def test_returns_200_with_normalized_data(self, client, mock_service):
        mock_service.get_accounts_info = AsyncMock(
            return_value=accounts_info_result_factory()
        )

        response = await client.get(
            "/api/v1/x/accounts",
            params={"usernames": "elonmusk", "provider_key": "twitterapi_io"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["username"] == "elonmusk"
        assert data["metadata"]["provider_key"] == "twitterapi_io"

    async def test_returns_422_when_usernames_missing(self, client):
        response = await client.get(
            "/api/v1/x/accounts",
            params={"provider_key": "twitterapi_io"},
        )

        assert response.status_code == 422

    async def test_returns_429_on_provider_rate_limit_error(self, client, mock_service):
        mock_service.get_accounts_info = AsyncMock(
            side_effect=ProviderRateLimitError("Rate limit exceeded")
        )

        response = await client.get(
            "/api/v1/x/accounts",
            params={"usernames": "elonmusk", "provider_key": "twitterapi_io"},
        )

        assert response.status_code == 429
        assert "detail" in response.json()
