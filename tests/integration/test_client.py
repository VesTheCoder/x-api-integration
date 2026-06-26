import httpx
import pytest
import respx
from app.core.exceptions import ProviderResponseError


@pytest.mark.integration
class TestTwitterAPIIOClientGetUserInfo:
    """
    Tests for TwitterAPIIOClient.get_user_info.
    """

    @respx.mock
    async def test_returns_payload_and_sends_correct_params(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/info").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"id": "123", "userName": "testuser"}},
            )
        )
        result = await twitter_client.get_user_info("testuser")

        assert result["data"]["id"] == "123"
        request = route.calls[0].request
        assert request.headers["X-API-Key"] == "test-key"
        assert request.url.params["userName"] == "testuser"

    @respx.mock
    async def test_raises_on_semantic_error(self, twitter_client):
        respx.get("https://test.twitterapi.io/twitter/user/info").mock(
            return_value=httpx.Response(
                200,
                json={"status": "error", "message": "Invalid API key"},
            )
        )

        with pytest.raises(ProviderResponseError, match="Invalid API key"):
            await twitter_client.get_user_info("testuser")

    @respx.mock
    async def test_raises_on_invalid_json(self, twitter_client):
        respx.get("https://test.twitterapi.io/twitter/user/info").mock(
            return_value=httpx.Response(200, text="not json")
        )

        with pytest.raises(ProviderResponseError, match="invalid JSON"):
            await twitter_client.get_user_info("testuser")

    @respx.mock
    async def test_raises_on_invalid_payload(self, twitter_client):
        respx.get("https://test.twitterapi.io/twitter/user/info").mock(
            return_value=httpx.Response(200, json=[1, 2, 3])
        )

        with pytest.raises(ProviderResponseError, match="invalid payload"):
            await twitter_client.get_user_info("testuser")


@pytest.mark.integration
class TestTwitterAPIIOClientGetUserLastTweets:
    """
    Tests for TwitterAPIIOClient.get_user_last_tweets param logic.
    """

    @respx.mock
    async def test_sends_userId_when_input_is_numeric(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/last_tweets").mock(
            return_value=httpx.Response(200, json={"data": {}})
        )
        await twitter_client.get_user_last_tweets("44196397")

        request = route.calls[0].request
        assert request.url.params["userId"] == "44196397"
        assert "userName" not in request.url.params

    @respx.mock
    async def test_sends_userName_when_input_is_username(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/last_tweets").mock(
            return_value=httpx.Response(200, json={"data": {}})
        )
        await twitter_client.get_user_last_tweets("elonmusk")

        request = route.calls[0].request
        assert request.url.params["userName"] == "elonmusk"
        assert "userId" not in request.url.params

    @respx.mock
    async def test_sends_includeReplies_when_enabled(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/last_tweets").mock(
            return_value=httpx.Response(200, json={"data": {}})
        )
        await twitter_client.get_user_last_tweets("elonmusk", include_replies=True)

        request = route.calls[0].request
        assert request.url.params["includeReplies"] == "true"

    @respx.mock
    async def test_sends_cursor_when_provided(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/last_tweets").mock(
            return_value=httpx.Response(200, json={"data": {}})
        )
        await twitter_client.get_user_last_tweets("elonmusk", cursor="abc123")

        request = route.calls[0].request
        assert request.url.params["cursor"] == "abc123"


@pytest.mark.integration
class TestTwitterAPIIOClientSearchUsers:
    """
    Tests for TwitterAPIIOClient.search_users.
    """

    @respx.mock
    async def test_sends_query_and_cursor(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/user/search").mock(
            return_value=httpx.Response(200, json={"users": []})
        )
        await twitter_client.search_users("elon", cursor="page2")

        request = route.calls[0].request
        assert request.url.params["query"] == "elon"
        assert request.url.params["cursor"] == "page2"


@pytest.mark.integration
class TestTwitterAPIIOClientGetTweetsByIds:
    """
    Tests for TwitterAPIIOClient.get_tweets_by_ids.
    """

    @respx.mock
    async def test_sends_tweet_ids(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/tweets").mock(
            return_value=httpx.Response(200, json={"tweets": []})
        )
        await twitter_client.get_tweets_by_ids("111,222")

        request = route.calls[0].request
        assert request.url.params["tweet_ids"] == "111,222"


@pytest.mark.integration
class TestTwitterAPIIOClientGetTweetReplies:
    """
    Tests for TwitterAPIIOClient.get_tweet_replies.
    """

    @respx.mock
    async def test_sends_tweet_id_with_time_filters(self, twitter_client):
        route = respx.get("https://test.twitterapi.io/twitter/tweet/replies").mock(
            return_value=httpx.Response(200, json={"tweets": []})
        )
        await twitter_client.get_tweet_replies(
            tweet_id="123", since=1000, until=2000, cursor=None
        )

        request = route.calls[0].request
        assert request.url.params["tweetId"] == "123"
        assert request.url.params["sinceTime"] == "1000"
        assert request.url.params["untilTime"] == "2000"
