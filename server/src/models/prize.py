from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.spin import Spin


class Prize(Base):
    __tablename__ = "prizes"

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true"
    )

    quantity: Mapped[int] = mapped_column(
        default=0,
        server_default="0"
    )

    spins: Mapped[list["Spin"]] = relationship(
        back_populates="prize",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="ck_prizes_quantity_non_negative"
        ),
    )

    def __str__(self) -> str:
        return f"Prize: #{self.id}"
