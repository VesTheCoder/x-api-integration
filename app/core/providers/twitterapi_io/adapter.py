from app.core.exceptions import ProviderResponseError, XAccountNotFoundError
from app.core.providers.twitterapi_io.schemas import TwitterAPIIOTweet, TwitterAPIIOUser
from app.schemas import XAccountInfo, XPost
from pydantic import ValidationError
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

        posts.extend(self._to_posts_from_raw_tweets(data.get("tweets")))
        return posts

    def to_posts(self, payload: dict[str, Any]) -> list[XPost]:
        """
        Convert raw tweets by IDs payload into normalized post list.
        """
        return self._to_posts_from_raw_tweets(payload.get("tweets"))

    def to_replies(self, payload: dict[str, Any]) -> list[XPost]:
        """
        Convert raw tweet replies payload into normalized post list.
        """
        return self._to_posts_from_raw_tweets(payload.get("tweets"))

    def _to_posts_from_raw_tweets(self, tweets: list[Any]) -> list[XPost]:
        """
        Convert a list of raw tweet dicts into normalized XPost list.
        """
        try:
            return [self._to_post_from_tweet(t) for t in tweets]

        except ValidationError as exc:
            raise ProviderResponseError(
                "Provider response has invalid tweet item"
            ) from exc

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

        handle = raw.user_name or raw.screen_name or ""

        return XAccountInfo(
            id=raw.id,
            username=handle,
            display_name=raw.name or handle,
            description=raw.description or None,
            description_url=raw.url or None,
            followers_count=raw.followers,
            following_count=raw.following,
            posts_count=raw.statuses_count,
            media_count=raw.media_count,
            location=raw.location or None,
            profile_image_url=raw.profile_picture or None,
            created_at=raw.created_at,
            is_verified=raw.verified,
            is_blue_verified=raw.is_blue_verified,
            account_url=f"https://x.com/intent/user?user_id={raw.id}",
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
            account_url=raw.author.url,
            is_reply=raw.is_reply,
            created_at=raw.created_at,
        )
