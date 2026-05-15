from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    app_name: str = Field(default="ClosedLoop OS", alias="APP_NAME")
    app_url: str = Field(default="http://localhost:3000", alias="APP_URL")
    api_url: str = Field(default="http://localhost:8000", alias="API_URL")
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    encryption_key: str = Field(default="change-me", alias="ENCRYPTION_KEY")
    database_url: str = Field(
        default="postgresql+asyncpg://closedloop:closedloop@localhost:5432/closedloop",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    kafka_bootstrap_servers: str = Field(default="localhost:9092", alias="KAFKA_BOOTSTRAP_SERVERS")
    azure_openai_endpoint: str = Field(default="", alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(default="", alias="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field(default="2024-10-21", alias="AZURE_OPENAI_API_VERSION")
    azure_openai_chat_deployment: str = Field(default="gpt-4o", alias="AZURE_OPENAI_CHAT_DEPLOYMENT")
    azure_openai_embedding_deployment: str = Field(
        default="text-embedding-3-large", alias="AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
    )
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
