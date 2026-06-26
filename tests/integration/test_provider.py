import pytest
from app.core.exceptions import ErrorCode, ProviderRateLimitError
from app.core.providers.twitterapi_io.provider import TwitterAPIIOProvider
from app.schemas import ErrorDTO, XAccountInfo, XPost
from tests.factories import (
    tweet_payload_factory,
    user_payload_factory,
    x_account_info_factory,
)
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.integration
class TestTwitterAPIIOProviderGetAccountsInfo:
    """
    Tests for TwitterAPIIOProvider.get_accounts_info.
    """

    async def test_returns_normalized_results_for_all_usernames(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.get_user_info = AsyncMock(
            side_effect=[
                user_payload_factory(),
                user_payload_factory(id="123", userName="cnn"),
            ]
        )
        provider.adapter.to_account_info = MagicMock(
            side_effect=[
                x_account_info_factory(),
                x_account_info_factory(id="123", username="cnn"),
            ]
        )

        result = await provider.get_accounts_info(["user1", "user2"])

        assert result.metadata.returned_count == 2
        assert result.metadata.error_code is None
        assert all(isinstance(r, XAccountInfo) for r in result.data)

    async def test_returns_partial_results_when_one_rate_limited(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.get_user_info = AsyncMock(
            side_effect=[
                user_payload_factory(),
                ProviderRateLimitError("Rate limit exceeded"),
            ]
        )
        provider.adapter.to_account_info = MagicMock(
            return_value=x_account_info_factory()
        )

        result = await provider.get_accounts_info(["user1", "user2"])

        assert result.metadata.returned_count == 1
        assert result.metadata.error_code == ErrorCode.RATE_LIMIT
        assert any(isinstance(r, ErrorDTO) for r in result.data)
        assert any(isinstance(r, XAccountInfo) for r in result.data)

    async def test_raises_when_all_usernames_rate_limited(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.get_user_info = AsyncMock(
            side_effect=ProviderRateLimitError("Rate limit exceeded")
        )

        with pytest.raises(ProviderRateLimitError):
            await provider.get_accounts_info(["user1"])


@pytest.mark.integration
class TestTwitterAPIIOProviderGetPosts:
    """
    Tests for TwitterAPIIOProvider.get_posts.
    """

    async def test_returns_normalized_posts(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.get_tweets_by_ids = AsyncMock(
            return_value={
                "tweets": [
                    tweet_payload_factory(id="111"),
                    tweet_payload_factory(id="222"),
                ]
            }
        )

        result = await provider.get_posts(["111", "222"])

        assert result.metadata.returned_count == 2
        assert all(isinstance(p, XPost) for p in result.data)
        assert result.data[0].id == "111"
        assert result.data[1].id == "222"


@pytest.mark.integration
class TestTwitterAPIIOProviderSearchAccounts:
    """
    Tests for TwitterAPIIOProvider.search_accounts.
    """

    async def test_returns_accounts_up_to_limit(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.search_users = AsyncMock(
            return_value={
                "users": [user_payload_factory()["data"]],
                "has_next_page": False,
            }
        )
        provider.adapter.to_accounts_search_results = MagicMock(
            return_value=[x_account_info_factory()]
        )

        result = await provider.search_accounts("elon", limit=1)

        assert result.metadata.returned_count == 1
        assert result.metadata.error_code is None

    async def test_returns_partial_results_when_rate_limited_after_first_page(
        self, adapter
    ):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.search_users = AsyncMock(
            side_effect=[
                {
                    "users": [user_payload_factory()["data"]],
                    "has_next_page": True,
                    "next_cursor": "abc",
                },
                ProviderRateLimitError("Rate limit exceeded"),
            ]
        )
        provider.adapter.to_accounts_search_results = MagicMock(
            return_value=[x_account_info_factory()]
        )

        result = await provider.search_accounts("elon", limit=10)

        assert result.metadata.returned_count == 1
        assert result.metadata.error_code == ErrorCode.RATE_LIMIT

    async def test_raises_when_rate_limited_on_first_page(self, adapter):
        provider = TwitterAPIIOProvider(
            client=AsyncMock(),
            adapter=adapter,
        )
        provider.client.search_users = AsyncMock(
            side_effect=ProviderRateLimitError("Rate limit exceeded")
        )

        with pytest.raises(ProviderRateLimitError):
            await provider.search_accounts("elon", limit=10)
