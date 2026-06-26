from app.schemas import (
    ProviderRunMetadata,
    XAccountInfo,
    XAccountsInfoResult,
    XProviderKey,
)
from datetime import UTC, datetime


def user_payload_factory(**overrides):
    """
    Build a valid TwitterAPI.io user payload with optional overrides.
    """
    base = {
        "data": {
            "id": "44196397",
            "userName": "elonmusk",
            "name": "Elon Musk",
            "description": "Technoking of Mars",
            "url": "https://x.com/elonmusk",
            "followers": 219000000,
            "following": 500,
            "statusesCount": 30000,
            "mediaCount": 5000,
            "location": "Mars",
            "profilePicture": "https://example.com/avatar.jpg",
            "createdAt": "2009-06-02T20:12:29.000Z",
            "verified": True,
            "isBlueVerified": True,
        }
    }
    base["data"].update(overrides)
    return base


def tweet_payload_factory(**overrides):
    """
    Build a valid TwitterAPI.io tweet payload with optional overrides.
    """
    base = {
        "id": "1893829352272113694",
        "text": "Mars, here we come.",
        "url": "https://x.com/elonmusk/status/1893829352272113694",
        "viewCount": 1500000,
        "likeCount": 250000,
        "retweetCount": 30000,
        "quoteCount": 5000,
        "replyCount": 12000,
        "isReply": False,
        "inReplyToId": None,
        "createdAt": "2025-02-20T15:30:00.000Z",
        "author": {
            "name": "elonmusk",
            "url": "https://x.com/elonmusk",
        },
    }
    base.update(overrides)
    return base


def x_account_info_factory(**overrides):
    """
    Build a valid XAccountInfo instance from hardcoded values.
    """
    defaults = {
        "id": "44196397",
        "username": "elonmusk",
        "display_name": "Elon Musk",
        "description": "Technoking of Mars",
        "description_url": "https://x.com/elonmusk",
        "followers_count": 219000000,
        "following_count": 500,
        "posts_count": 30000,
        "media_count": 5000,
        "location": "Mars",
        "profile_image_url": "https://example.com/avatar.jpg",
        "created_at": "2009-06-02T20:12:29.000Z",
        "is_verified": True,
        "is_blue_verified": True,
        "account_url": "https://x.com/intent/user?user_id=44196397",
    }
    defaults.update(overrides)
    return XAccountInfo(**defaults)


def _metadata_factory(**overrides):
    """
    Build a valid ProviderRunMetadata instance from hardcoded values.
    """
    defaults = {
        "provider_key": XProviderKey.twitterapi_io,
        "input_query": "elonmusk",
        "latency_ms": 150,
        "estimated_cost_usd": 0.00015,
        "requested_limit": 1,
        "returned_count": 1,
        "fetched_at": datetime(2025, 6, 26, 10, 0, 0, tzinfo=UTC),
        "error_code": None,
        "error_message": None,
    }
    defaults.update(overrides)
    return ProviderRunMetadata(**defaults)


def accounts_info_result_factory(**overrides):
    """
    Build a valid XAccountsInfoResult instance from hardcoded values.
    """
    data = overrides.pop("data", [x_account_info_factory()])
    metadata = overrides.pop("metadata", _metadata_factory())
    return XAccountsInfoResult(data=data, metadata=metadata, **overrides)


def x_api_response_log_factory(**overrides):
    """
    Build kwargs for XApiResponseRepository.create_log from hardcoded values.
    """
    defaults = {
        "endpoint": "get_accounts_info",
        "request_params": {"usernames": ["elonmusk"]},
        "response_data": {"data": [{"id": "44196397"}]},
        "response_metadata": {"latency_ms": 150},
        "error_snapshot": None,
    }
    defaults.update(overrides)
    return defaults
