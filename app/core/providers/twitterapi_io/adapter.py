from app.core.exceptions import ProviderResponseError, XAccountNotFoundError
from app.schemas import XAccountInfo
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

    def _extract_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        user = payload.get("data") or payload.get("user") or payload
        if not isinstance(user, dict):
            raise ProviderResponseError("Provider response has invalid user data")
        if user.get("unavailable"):
            reason = self._get_str(user, "unavailableReason")
            raise XAccountNotFoundError(reason or "X account is unavailable")
        return user

    def _to_account_info_from_user(self, user: dict[str, Any]) -> XAccountInfo:
        username = (
            self._get_str(user, "userName")
            or self._get_str(user, "screen_name")
            or self._get_str(user, "username")
        )
        if not username:
            raise ProviderResponseError("Provider response has no username")
        return XAccountInfo(
            id=self._get_str(user, "id"),
            username=username,
            display_name=self._get_str(user, "name") or username,
            description=self._get_str(user, "description"),
            url=self._get_str(user, "url") or f"https://x.com/{username}",
            followers_count=self._get_int(user, "followers", "followers_count"),
            following_count=self._get_int(
                user,
                "following",
                "following_count",
                "friends_count",
            ),
            posts_count=self._get_int(user, "statusesCount", "statuses_count"),
            media_count=self._get_opt_int(user, "mediaCount", "media_tweets_count"),
            location=self._get_str(user, "location"),
            profile_image_url=self._get_str(
                user,
                "profilePicture",
                "profile_image_url_https",
            ),
            created_at=self._get_str(user, "createdAt", "created_at"),
            is_verified=self._get_opt_bool(user, "verified"),
            is_blue_verified=self._get_opt_bool(user, "isBlueVerified"),
        )

    def _get_str(self, payload: dict[str, Any], *keys: str) -> str:
        for key in keys:
            value = payload.get(key)
            if value is not None:
                return str(value)
        return ""

    def _get_int(self, payload: dict[str, Any], *keys: str) -> int:
        for key in keys:
            value = payload.get(key)
            if value is not None:
                return int(value)
        return 0

    def _get_opt_int(self, payload: dict[str, Any], *keys: str) -> int | None:
        for key in keys:
            value = payload.get(key)
            if value is not None:
                return int(value)
        return None

    def _get_opt_bool(self, payload: dict[str, Any], *keys: str) -> bool | None:
        for key in keys:
            value = payload.get(key)
            if value is not None:
                return bool(value)
        return None
