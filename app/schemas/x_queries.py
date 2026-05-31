from app.schemas.x_base import XPaginatedQuery, XPostSearchSorting, XQuery
from datetime import datetime
from pydantic import Field


class GetAccountInfoQuery(XQuery):
    pass


class SearchAccountsQuery(XPaginatedQuery):
    query: str
    max_runtime_sec: int | None = Field(default=None, ge=1)


class GetAccountPostsQuery(XPaginatedQuery):
    username_or_userid: str
    include_replies: bool = False


class GetPostsQuery(XQuery):
    urls_or_ids: str


class SearchPostsQuery(XPaginatedQuery):
    query: str
    since: datetime | None = None
    until: datetime | None = None
    sorting: XPostSearchSorting = XPostSearchSorting.latest


class GetRepliesQuery(XPaginatedQuery):
    url_or_id: str
    since: datetime | None = None
    until: datetime | None = None
