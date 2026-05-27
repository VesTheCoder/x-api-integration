from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSConfig(BaseSettings):
    """
    CORS middleware configuration.
    Reads CORS_* variables from environment.
    """

    model_config = SettingsConfigDict(env_prefix="CORS_")
    origins: list[str] = Field(default_factory=list)
    allow_credentials: bool = Field(default=False)
    allow_methods: list[str] = Field(default=["*"])
    allow_headers: list[str] = Field(default=["*"])
    max_age: int = Field(default=600)


class XProviders(BaseSettings):
    """
    X/Twitter provider API keys and configuration.
    Each provider has its own prefixed environment variables.
    """

    model_config = SettingsConfigDict(env_prefix="PROVIDER_X_")
    twitterapi_io: str = Field(default="")


class Settings(BaseSettings):
    """
    Main application settings with nested configs.
    Reads APP_HOST and APP_PORT from environment.
    """

    model_config = SettingsConfigDict(env_prefix="APP_")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    cors: CORSConfig = Field(default_factory=CORSConfig)
    providers: XProviders = Field(default_factory=XProviders)
