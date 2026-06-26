import pytest
from app.core.exceptions import ProviderResponseError, XAccountNotFoundError
from tests.factories import tweet_payload_factory, user_payload_factory


@pytest.mark.unit
class TestToAccountInfo:
    """
    Tests for TwitterAPIIOAdapter.to_account_info.
    """

    def test_maps_valid_user_payload_to_account_info(self, adapter):
        result = adapter.to_account_info(user_payload_factory())

        assert result.id == "44196397"
        assert result.username == "elonmusk"
        assert result.display_name == "Elon Musk"
        assert result.followers_count == 219000000
        assert result.following_count == 500
        assert result.posts_count == 30000
        assert result.media_count == 5000
        assert result.is_verified is True
        assert result.is_blue_verified is True
        assert result.description == "Technoking of Mars"
        assert result.location == "Mars"
        assert result.profile_image_url == "https://example.com/avatar.jpg"
        assert result.account_url == "https://x.com/intent/user?user_id=44196397"

    def test_raises_not_found_when_user_unavailable(self, adapter):
        payload = {
            "data": {
                "unavailable": True,
                "unavailableReason": "suspended",
            }
        }

        with pytest.raises(XAccountNotFoundError, match="suspended"):
            adapter.to_account_info(payload)

    def test_raises_response_error_when_invalid_user_data(self, adapter):
        payload = {"data": "not a dict"}

        with pytest.raises(ProviderResponseError, match="invalid user data"):
            adapter.to_account_info(payload)


@pytest.mark.unit
class TestToAccountsSearchResults:
    """
    Tests for TwitterAPIIOAdapter.to_accounts_search_results.
    """

    def test_skips_unavailable_users_in_search_results(self, adapter):
        available = user_payload_factory()["data"]
        unavailable = {"unavailable": True, "unavailableReason": "protected"}
        payload = {"users": [available, unavailable]}

        results = adapter.to_accounts_search_results(payload)

        assert len(results) == 1
        assert results[0].id == "44196397"

    def test_raises_response_error_when_users_not_list(self, adapter):
        payload = {"users": "not a list"}

        with pytest.raises(ProviderResponseError, match="invalid users data"):
            adapter.to_accounts_search_results(payload)

    def test_raises_response_error_when_user_item_not_dict(self, adapter):
        payload = {"users": ["not a dict"]}

        with pytest.raises(ProviderResponseError, match="invalid user item"):
            adapter.to_accounts_search_results(payload)


@pytest.mark.unit
class TestToAccountPosts:
    """
    Tests for TwitterAPIIOAdapter.to_account_posts.
    """

    def test_maps_tweets_with_pin_tweet_first(self, adapter):
        pin = tweet_payload_factory(id="111")
        tweet = tweet_payload_factory(id="222")
        payload = {"data": {"pin_tweet": pin, "tweets": [tweet]}}

        results = adapter.to_account_posts(payload)

        assert len(results) == 2
        assert results[0].id == "111"
        assert results[1].id == "222"

    def test_maps_tweets_without_pin_tweet(self, adapter):
        tweet = tweet_payload_factory(id="222")
        payload = {"data": {"tweets": [tweet]}}

        results = adapter.to_account_posts(payload)

        assert len(results) == 1
        assert results[0].id == "222"

    def test_raises_response_error_when_data_not_dict(self, adapter):
        payload = {"data": "not a dict"}

        with pytest.raises(ProviderResponseError, match="invalid tweets data"):
            adapter.to_account_posts(payload)


@pytest.mark.unit
class TestToPosts:
    """
    Tests for TwitterAPIIOAdapter.to_posts.
    """

    def test_maps_tweets_by_ids(self, adapter):
        payload = {
            "tweets": [
                tweet_payload_factory(id="111"),
                tweet_payload_factory(id="222"),
            ]
        }

        results = adapter.to_posts(payload)

        assert len(results) == 2
        assert results[0].id == "111"
        assert results[1].id == "222"

    def test_returns_empty_list_when_no_tweets(self, adapter):
        results = adapter.to_posts({"tweets": []})

        assert results == []


@pytest.mark.unit
class TestToSearchPosts:
    """
    Tests for TwitterAPIIOAdapter.to_search_posts.
    """

    def test_maps_search_tweets(self, adapter):
        payload = {
            "tweets": [
                tweet_payload_factory(id="111"),
                tweet_payload_factory(id="222"),
            ]
        }

        results = adapter.to_search_posts(payload)

        assert len(results) == 2
        assert results[0].id == "111"
        assert results[1].id == "222"


@pytest.mark.unit
class TestToReplies:
    """
    Tests for TwitterAPIIOAdapter.to_replies.
    """

    def test_maps_replies(self, adapter):
        payload = {
            "tweets": [
                tweet_payload_factory(id="111"),
                tweet_payload_factory(id="222"),
            ]
        }

        results = adapter.to_replies(payload)

        assert len(results) == 2
        assert results[0].id == "111"
        assert results[1].id == "222"
