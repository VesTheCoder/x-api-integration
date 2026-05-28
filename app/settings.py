from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """
    PostgreSQL database configuration.
    Reads POSTGRES_* variables from environment.
    """

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    db: str = Field(default="x_api_integration")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")

    @computed_field
    @property
    def database_url(self) -> str:
        """
        Generate PostgreSQL async connection URL.
        """
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password}@{self.host}:{self.port}/{self.db}"
        )


class XProviders(BaseSettings):
    """
    X/Twitter provider API keys and configuration.
    Each provider has its own prefixed environment variables.
    """

    model_config = SettingsConfigDict(env_prefix="PROVIDER_X_")
    twitterapi_io_api_key: str = Field(min_length=1)
    twitterapi_io_base_url: str = Field(min_length=1)


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
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
