from pydantic import BaseModel, Field, model_validator


class TwitterAPIIOUser(BaseModel):
    """
    Raw user response from TwitterAPI.io.
    """

    id: str = ""
    user_name: str | None = Field(default=None, alias="userName")
    screen_name: str = Field(default="", alias="screenName")
    name: str = ""
    description: str | None = None
    url: str | None = None
    followers: int = 0
    following: int = 0
    statuses_count: int = Field(default=0, alias="statusesCount")
    media_count: int | None = Field(default=None, alias="mediaCount")
    location: str | None = None
    profile_picture: str | None = Field(default=None, alias="profilePicture")
    created_at: str = Field(default="", alias="createdAt")
    verified: bool | None = None
    is_blue_verified: bool | None = Field(default=None, alias="isBlueVerified")
    unavailable_reason: str = Field(default="", alias="unavailableReason")

    @model_validator(mode="before")
    @classmethod
    def _normalize_keys(cls, data: dict) -> dict:
        _pick_first(data, "followers", ["followers_count"])
        _pick_first(data, "following", ["following_count", "friends_count"])
        _pick_first(data, "statusesCount", ["statuses_count"])
        _pick_first(data, "mediaCount", ["media_tweets_count"])
        _pick_first(data, "profilePicture", ["profile_image_url_https"])
        _pick_first(data, "createdAt", ["created_at"])
        return data


class TwitterAPIIOAuthor(BaseModel):
    """
    Raw author object inside tweet.
    """

    name: str = ""
    url: str = ""


class TwitterAPIIOTweet(BaseModel):
    """
    Raw tweet response from TwitterAPI.io.
    """

    id: str = ""
    text: str = ""
    url: str = ""
    view_count: int = Field(default=0, alias="viewCount")
    like_count: int = Field(default=0, alias="likeCount")
    retweet_count: int = Field(default=0, alias="retweetCount")
    quote_count: int = Field(default=0, alias="quoteCount")
    reply_count: int = Field(default=0, alias="replyCount")
    created_at: str = Field(default="", alias="createdAt")
    author: TwitterAPIIOAuthor = Field(default_factory=TwitterAPIIOAuthor)


def _pick_first(data: dict, target: str, candidates: list[str]) -> None:
    if target not in data or data[target] in (None, ""):
        for key in candidates:
            if key in data and data[key] not in (None, ""):
                data[target] = data[key]
                break
