from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.database import Base


class Admin(Base):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true"
    )

    def __str__(self) -> str:
        return f"Admin: #{self.id}"
