from pydantic import BaseModel
from pydantic import ConfigDict


class PrizeRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
