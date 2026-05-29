from app.core.exceptions import ProviderResponseError, XAccountNotFoundError
from app.core.providers.twitterapi_io.schemas import TwitterAPIIOTweet, TwitterAPIIOUser
from app.schemas import XAccountInfo, XPost
from typing import Any


class TwitterAPIIOAdapter:
    """
    Converts TwitterAPI.io payloads into normalized DTOs.
    """

    def to_account_info(self, payload: dict[str, Any]) -> XAccountInfo:
        """
        Convert raw user payload into normalized account info.
        """
        user = self._extract_user(payload)
        return self._to_account_info_from_user(user)

    def to_accounts_search_results(self, payload: dict[str, Any]) -> list[XAccountInfo]:
        """
        Convert raw search payload into normalized account list.
        """
        users = payload.get("users")

        if not isinstance(users, list):
            raise ProviderResponseError("Provider response has invalid users data")

        accounts: list[XAccountInfo] = []

        for item in users:
            if not isinstance(item, dict):
                raise ProviderResponseError("Provider response has invalid user item")

            if item.get("unavailable"):
                continue

            accounts.append(self._to_account_info_from_user(item))

        return accounts

    def to_account_posts(self, payload: dict[str, Any]) -> list[XPost]:
        """
        Convert raw tweets payload into normalized post list.
        """
        data = payload.get("data") or payload

        if not isinstance(data, dict):
            raise ProviderResponseError("Provider response has invalid tweets data")

        posts: list[XPost] = []
        pin_tweet = data.get("pin_tweet")

        if isinstance(pin_tweet, dict):
            posts.append(self._to_post_from_tweet(pin_tweet))

        tweets = data.get("tweets")

        if not isinstance(tweets, list):
            raise ProviderResponseError("Provider response has invalid tweets data")

        for tweet in tweets:
            if not isinstance(tweet, dict):
                raise ProviderResponseError("Provider response has invalid tweet item")

            posts.append(self._to_post_from_tweet(tweet))

        return posts

    def to_posts(self, payload: dict[str, Any]) -> list[XPost]:
        """
        Convert raw tweets by IDs payload into normalized post list.
        """
        tweets = payload.get("tweets")

        if not isinstance(tweets, list):
            raise ProviderResponseError("Provider response has invalid tweets data")

        posts: list[XPost] = []

        for tweet in tweets:
            if not isinstance(tweet, dict):
                raise ProviderResponseError("Provider response has invalid tweet item")

            posts.append(self._to_post_from_tweet(tweet))

        return posts

    def _extract_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        user = payload.get("data") or payload.get("user") or payload

        if not isinstance(user, dict):
            raise ProviderResponseError("Provider response has invalid user data")

        if user.get("unavailable"):
            reason = TwitterAPIIOUser.model_validate(user).unavailable_reason
            raise XAccountNotFoundError(reason or "X account is unavailable")

        return user

    def _to_account_info_from_user(self, user: dict[str, Any]) -> XAccountInfo:
        raw = TwitterAPIIOUser.model_validate(user)

        if not raw.user_name:
            raise ProviderResponseError("Provider response has no username")

        return XAccountInfo(
            id=raw.id,
            username=raw.user_name,
            display_name=raw.name or raw.user_name,
            description=raw.description,
            url=raw.url or f"https://x.com/{raw.user_name}",
            followers_count=raw.followers,
            following_count=raw.following,
            posts_count=raw.statuses_count,
            media_count=raw.media_count,
            location=raw.location,
            profile_image_url=raw.profile_picture,
            created_at=raw.created_at,
            is_verified=raw.verified,
            is_blue_verified=raw.is_blue_verified,
        )

    def _to_post_from_tweet(self, tweet: dict[str, Any]) -> XPost:
        """
        Convert a single raw tweet dict into normalized XPost.
        """
        raw = TwitterAPIIOTweet.model_validate(tweet)

        return XPost(
            id=raw.id,
            text=raw.text,
            url=raw.url,
            views=raw.view_count,
            likes=raw.like_count,
            retweets=raw.retweet_count,
            quotes=raw.quote_count,
            replies=raw.reply_count,
            account_name=raw.author.name,
            account_link=raw.author.url,
            created_at=raw.created_at,
        )
