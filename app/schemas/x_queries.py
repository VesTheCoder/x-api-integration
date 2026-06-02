from app.core.utils import (
    normalize_single_tweet_id,
    normalize_tweet_ids,
    normalize_usernames,
)
from app.schemas.x_base import XPaginatedQuery, XPostSearchSorting, XQuery
from datetime import datetime
from pydantic import Field, field_validator


class GetAccountsInfoQuery(XQuery):
    usernames: list[str]

    @field_validator("usernames", mode="before")
    @classmethod
    def _normalize(cls, v: list[str]) -> list[str]:
        return normalize_usernames(v)


class SearchAccountsQuery(XPaginatedQuery):
    query: str
    max_runtime_sec: int | None = Field(default=None, ge=1)


class GetAccountPostsQuery(XPaginatedQuery):
    username_or_userid: str
    include_replies: bool = False


class GetPostsQuery(XQuery):
    tweet_ids: list[str]

    @field_validator("tweet_ids", mode="before")
    @classmethod
    def _normalize(cls, v: list[str]) -> list[str]:
        return normalize_tweet_ids(v)


class SearchPostsQuery(XPaginatedQuery):
    query: str
    since: datetime | None = None
    until: datetime | None = None
    sorting: XPostSearchSorting = XPostSearchSorting.latest
    include_replies: bool = False


class GetRepliesQuery(XPaginatedQuery):
    url_or_id: str
    since: datetime | None = None
    until: datetime | None = None

    @field_validator("url_or_id", mode="before")
    @classmethod
    def _normalize(cls, v: str) -> str:
        return normalize_single_tweet_id(v)
