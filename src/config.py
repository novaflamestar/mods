from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    DISCORD_BOT_TOKEN: str
    DISCORD_GUILD_ID: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5432


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
