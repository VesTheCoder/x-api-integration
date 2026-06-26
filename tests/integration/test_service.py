import pytest
from app.core.exceptions import ProviderRateLimitError
from tests.factories import accounts_info_result_factory
from unittest.mock import AsyncMock


@pytest.mark.integration
class TestXServiceGetAccountsInfo:
    """
    Tests for XService.get_accounts_info.
    """

    async def test_delegates_to_provider_and_persists_result(
        self, service, mock_provider, mock_repo
    ):
        expected = accounts_info_result_factory()
        mock_provider.get_accounts_info = AsyncMock(return_value=expected)

        result = await service.get_accounts_info(mock_provider, ["elonmusk"])

        assert result == expected
        mock_provider.get_accounts_info.assert_called_once_with(["elonmusk"])
        mock_repo.create_log.assert_called_once()
        call_kwargs = mock_repo.create_log.call_args.kwargs
        assert call_kwargs["endpoint"] == "get_accounts_info"
        assert call_kwargs["error_snapshot"] is None

    async def test_persists_error_and_reraises_on_failure(
        self, service, mock_provider, mock_repo
    ):
        error = ProviderRateLimitError("Rate limit")
        mock_provider.get_accounts_info = AsyncMock(side_effect=error)

        with pytest.raises(ProviderRateLimitError):
            await service.get_accounts_info(mock_provider, ["elonmusk"])

        mock_repo.create_log.assert_called_once()
        call_kwargs = mock_repo.create_log.call_args.kwargs
        assert call_kwargs["error_snapshot"] is not None
        assert call_kwargs["response_data"] is None
