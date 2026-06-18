from enum import StrEnum
from pydantic import BaseModel, Field


class XProviderKey(StrEnum):
    twitterapi_io = "twitterapi_io"


class XQuery(BaseModel):
    provider_key: XProviderKey = Field(default=XProviderKey.twitterapi_io)


class XPaginatedQuery(XQuery):
    """
    Base query for paginated X endpoints.
    """

    limit: int | None = Field(default=None, ge=20)


class XPostSearchSorting(StrEnum):
    latest = "Latest"
    top = "Top"
