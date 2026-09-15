from pydantic import BaseModel
from pydantic import ConfigDict


class UserRead(BaseModel):
    id: int
    telegram_id: int
    username: str | None

    model_config = ConfigDict(from_attributes=True)
