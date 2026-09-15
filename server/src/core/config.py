from pathlib import Path
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(default=...)
    POSTGRES_PASSWORD: SecretStr = Field(default=...)
    POSTGRES_HOST: str = Field(default=...)
    POSTGRES_PORT: int = Field(default=...)
    POSTGRES_DB: str = Field(default=...)

    ADMIN_TITLE: str = Field(default="Biomirix Admin")
    ADMIN_SECRET_KEY: SecretStr = Field(default=SecretStr("change-me"))

    BOT_TOKEN: SecretStr = Field(default=...)
    TELEGRAM_INIT_DATA_MAX_AGE_SECONDS: int = Field(default=86400)

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8"
    )

settings = Settings()
