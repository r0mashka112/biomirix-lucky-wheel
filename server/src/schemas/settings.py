from pydantic import BaseModel


class PublicSettingsRead(BaseModel):
    greeting_message: str | None
