from fastapi import APIRouter

from src.deps import SessionDependence
from src.schemas.settings import PublicSettingsRead
from src.services.settings import get_greeting_message

router = APIRouter()


@router.get("/public", response_model=PublicSettingsRead)
async def get_public_settings(
    session: SessionDependence,
) -> PublicSettingsRead:
    return PublicSettingsRead(
        greeting_message=await get_greeting_message(session),
    )
