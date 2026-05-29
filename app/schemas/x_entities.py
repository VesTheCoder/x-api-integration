from app.schemas.x_queries import XProviderKey
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
    requested_limit: int
    returned_count: int


class XAccountInfo(BaseModel):
    id: str
    username: str
    display_name: str
    description: str
    url: str
    followers_count: int
    following_count: int
    posts_count: int
    media_count: int | None = None
    location: str
    profile_image_url: str
    created_at: str
    is_verified: bool | None = None
    is_blue_verified: bool | None = None


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
    account_link: str
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
