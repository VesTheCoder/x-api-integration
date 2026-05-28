from enum import StrEnum
from pydantic import BaseModel, Field


class XProviderKey(StrEnum):
    twitterapi_io = "twitterapi_io"


class XQuery(BaseModel):
    provider_key: XProviderKey = Field(default=XProviderKey.twitterapi_io)


class GetAccountInfoQuery(XQuery):
    pass


class SearchAccountsQuery(XQuery):
    query: str
    limit: int = Field(ge=10)
    max_runtime_sec: int | None = Field(default=None, ge=1)
