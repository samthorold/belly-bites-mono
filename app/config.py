import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", ".env"), env_file_encoding="utf-8"
    )
    LOG_LEVEL: str = "DEBUG"

    APP_NAME: str = "Belly Bites"
    APP_SECRET_KEY: str = ""

    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: str = ""
    AUTH0_DOMAIN: str = ""
