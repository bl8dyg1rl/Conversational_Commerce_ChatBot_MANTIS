from pathlib import Path

from pydantic_settings import BaseSettings


ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):

    telegram_bot_token: str

    class Config:
        env_file = ENV_FILE
        extra = "ignore"


settings = Settings()