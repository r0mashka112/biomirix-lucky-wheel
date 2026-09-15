from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy import BigInteger

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.spin import Spin


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
    )

    username: Mapped[str | None] = mapped_column(String(255))

    spin: Mapped["Spin | None"] = relationship(
        back_populates="user",
        passive_deletes=True,
        uselist=False
    )

    def __str__(self) -> str:
        return f"User: #{self.id}"
