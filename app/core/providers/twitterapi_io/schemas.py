from pydantic import BaseModel, Field


class TwitterAPIIOUser(BaseModel):
    """
    Raw user response from TwitterAPI.io.
    """

    id: str = ""
    user_name: str = Field(default="", alias="userName")
    name: str = ""
    description: str = ""
    url: str = ""
    followers: int = 0
    following: int = 0
    statuses_count: int = Field(default=0, alias="statusesCount")
    media_count: int | None = Field(default=None, alias="mediaCount")
    location: str = ""
    profile_picture: str = Field(default="", alias="profilePicture")
    created_at: str = Field(default="", alias="createdAt")
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
    created_at: str = Field(default="", alias="createdAt")
    author: TwitterAPIIOAuthor = Field(default_factory=TwitterAPIIOAuthor)
