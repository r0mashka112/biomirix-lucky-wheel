from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.database import Base


class AppSettings(Base):
    __tablename__ = "app_settings"

    greeting_message: Mapped[str | None] = mapped_column(Text)
    post_spin_message: Mapped[str | None] = mapped_column(Text)

    def __str__(self) -> str:
        return "App Settings"
