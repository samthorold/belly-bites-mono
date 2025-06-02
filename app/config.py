import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", ".env"), env_file_encoding="utf-8"
    )
    LOG_LEVEL: str = "DEBUG"

    APP_NAME: str = "Belly Bites"
    APP_SECRET_KEY: SecretStr = SecretStr("")

    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: SecretStr = SecretStr("")
    AUTH0_DOMAIN: str = ""
