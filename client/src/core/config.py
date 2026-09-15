from pathlib import Path

from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(default=...)
    BASE_URL: str = Field(default=...)
    BACKEND_API_URL: str = Field(default=...)
    TELEGRAM_CHANNEL_ID: int = Field(default=...)
    TELEGRAM_CHANNEL_URL: str = Field(default=...)

    GREETING_MESSAGE: str = (
        "Добро пожаловать в бот розыгрыша от <strong>Biomirix!</strong> "
        "Победители будут определены мгновенно — удачи!"
    )

    MESSAGE_IF_SUBSCRIBED: str = "Нажмите на кнопку ниже, чтобы запустить колесо фортуны"

    MESSAGE_IF_NOT_SUBSCRIBED: str = (
        "Для <strong>участия</strong> в розыгрыше нужно "
        "<strong>подписаться</strong> на наш Telegram канал"
    )

    MESSAGE_IF_NOT_UNDERSTAND: str = "К сожалению, не понял вас"

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}/webhook"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
