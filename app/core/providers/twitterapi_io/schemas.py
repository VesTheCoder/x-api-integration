from pydantic import AliasChoices, BaseModel, Field


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
    followers: int = Field(
        default=0,
        validation_alias=AliasChoices("followers", "followers_count"),
    )
    following: int = Field(
        default=0,
        validation_alias=AliasChoices("following", "following_count", "friends_count"),
    )
    statuses_count: int = Field(
        default=0,
        alias="statusesCount",
        validation_alias=AliasChoices("statusesCount", "statuses_count"),
    )
    media_count: int | None = Field(
        default=None,
        alias="mediaCount",
        validation_alias=AliasChoices("mediaCount", "media_tweets_count"),
    )
    location: str | None = None
    profile_picture: str | None = Field(
        default=None,
        alias="profilePicture",
        validation_alias=AliasChoices("profilePicture", "profile_image_url_https"),
    )
    created_at: str = Field(
        default="",
        alias="createdAt",
        validation_alias=AliasChoices("createdAt", "created_at"),
    )
    verified: bool | None = None
    is_blue_verified: bool | None = Field(default=None, alias="isBlueVerified")
    unavailable_reason: str = Field(default="", alias="unavailableReason")


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
    is_reply: bool = Field(default=False, alias="isReply")
    in_reply_to_id: str | None = Field(default=None, alias="inReplyToId")
    created_at: str = Field(default="", alias="createdAt")
    author: TwitterAPIIOAuthor = Field(default_factory=TwitterAPIIOAuthor)
