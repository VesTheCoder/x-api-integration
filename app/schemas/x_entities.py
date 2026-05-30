from app.schemas.x_base import XProviderKey
from datetime import datetime
from pydantic import BaseModel


class ProviderRunMetadata(BaseModel):
    provider_key: XProviderKey
    provider_run_id: str | None = None
    input_query: str
    latency_ms: int
    error_code: int | None = None
    error_message: str | None = None
    fetched_at: datetime


class XSearchMetadata(ProviderRunMetadata):
    requested_limit: int | None
    returned_count: int


class XAccountInfo(BaseModel):
    id: str
    username: str
    display_name: str
    description: str | None = None
    description_url: str | None = None
    followers_count: int
    following_count: int
    posts_count: int
    media_count: int | None = None
    location: str | None = None
    profile_image_url: str | None = None
    created_at: str
    is_verified: bool | None = None
    is_blue_verified: bool | None = None
    account_url: str


class XPost(BaseModel):
    id: str
    text: str
    url: str
    views: int
    likes: int
    retweets: int
    quotes: int
    replies: int
    account_name: str
    account_url: str
    is_reply: bool
    created_at: str


class XAccountInfoResult(BaseModel):
    data: XAccountInfo
    metadata: ProviderRunMetadata


class XAccountsSearchResult(BaseModel):
    data: list[XAccountInfo]
    metadata: XSearchMetadata


class XPostsResult(BaseModel):
    data: list[XPost]
    metadata: ProviderRunMetadata
