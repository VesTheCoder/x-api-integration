from app.core.exceptions import ProviderResponseError, XAccountNotFoundError
from app.schemas.x_entities import XAccountInfo
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
        username = self._get_str(user, "userName") or self._get_str(user, "username")
        if not username:
            raise ProviderResponseError("Provider response has no username")
        return XAccountInfo(
            id=self._get_str(user, "id"),
            username=username,
            display_name=self._get_str(user, "name") or username,
            description=self._get_str(user, "description"),
            url=self._get_str(user, "url") or f"https://x.com/{username}",
            followers_count=self._get_int(user, "followers"),
            following_count=self._get_int(user, "following"),
            posts_count=self._get_int(user, "statusesCount"),
            media_count=self._get_opt_int(user, "mediaCount"),
            location=self._get_str(user, "location"),
            profile_image_url=self._get_str(user, "profilePicture"),
            created_at=self._get_str(user, "createdAt"),
            is_verified=self._get_opt_bool(user, "verified"),
            is_blue_verified=self._get_opt_bool(user, "isBlueVerified"),
        )

    def _extract_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        user = payload.get("data") or payload.get("user") or payload
        if not isinstance(user, dict):
            raise ProviderResponseError("Provider response has invalid user data")
        if user.get("unavailable"):
            reason = self._get_str(user, "unavailableReason")
            raise XAccountNotFoundError(reason or "X account is unavailable")
        return user

    def _get_str(self, payload: dict[str, Any], key: str) -> str:
        value = payload.get(key)
        return str(value) if value is not None else ""

    def _get_int(self, payload: dict[str, Any], key: str) -> int:
        value = payload.get(key)
        return int(value) if value is not None else 0

    def _get_opt_int(self, payload: dict[str, Any], key: str) -> int | None:
        value = payload.get(key)
        return int(value) if value is not None else None

    def _get_opt_bool(self, payload: dict[str, Any], key: str) -> bool | None:
        value = payload.get(key)
        return bool(value) if value is not None else None
