from typing import TYPE_CHECKING

from sqlalchemy import Index
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.prize import Prize


class Spin(Base):
    __tablename__ = "spins"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    prize_id: Mapped[int] = mapped_column(
        ForeignKey("prizes.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(
        back_populates="spin"
    )

    prize: Mapped["Prize"] = relationship(
        back_populates="spins"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_spins_user"
        ),

        Index(
            "ix_spins_prize_id",
            "prize_id"
        ),
    )

    def __str__(self) -> str:
        return f"Spin: #{self.id}"
