import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", ".env"), env_file_encoding="utf-8"
    )
    APP_NAME: str = "Belly Bites"
    LOG_LEVEL: str = "DEBUG"
