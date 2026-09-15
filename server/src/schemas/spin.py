from pydantic import BaseModel

from src.schemas.prize import PrizeRead


class SpinRead(BaseModel):
    id: int
    prize: PrizeRead


class SpinStatusRead(BaseModel):
    can_spin: bool
    reason: str | None
    spin: SpinRead | None


class SpinCreateResponse(BaseModel):
    spin_id: int
    prize: PrizeRead
