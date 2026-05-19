from pathlib import Path
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_URL: str
    BACKEND_URL: str
    CHAT_ID: int

    GREETING_MESSAGE: str = (
        'Добро пожаловать в бот розыгрыша от <strong>Biomirix!</strong> '
        'Победители будут определены мгновенно — удачи!'
    )

    MESSAGE_IF_SUBSCRIBED: str = 'Нажмите на кнопку ниже, чтобы запустить колесо фортуны'

    MESSAGE_IF_NOT_SUBSCRIBED: str = (
        'Для <strong>участия</strong> в розыгрыше нужно '
        '<strong>подписаться</strong> на наш Telegram канал'
    )

    MESSAGE_IF_NOT_UNDERSTAND: str = 'К сожалению, не понял вас'

    @property
    def WEBHOOK_URL(self) -> str:
        return f'{self.BASE_URL}/webhook'

    model_config = SettingsConfigDict(
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

settings = Settings()