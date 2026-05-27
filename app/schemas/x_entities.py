from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class XProviderKey(StrEnum):
    twitterapi_io = "twitterapi_io"


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


class ProviderRunMetadata(BaseModel):
    provider_key: XProviderKey
    provider_run_id: str | None = None
    input_query: str
    estimated_cost: float | None = None
    actual_cost: float | None = None
    latency_ms: int
    error_code: str | None = None
    error_message: str | None = None
    fetched_at: datetime


class XAccountInfoResult(BaseModel):
    data: XAccountInfo
    metadata: ProviderRunMetadata
