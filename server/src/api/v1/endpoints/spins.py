from fastapi import APIRouter

from src.api.deps import UserDependence
from src.deps import SessionDependence
from src.integrations.telegram import send_message
from src.integrations.telegram import send_prize_message
from src.schemas.prize import PrizeRead
from src.schemas.spin import SpinCreateResponse
from src.services.settings import get_post_spin_message
from src.services.spins import create_spin

router = APIRouter()


@router.post("", response_model=SpinCreateResponse)
async def create_user_spin(
    session: SessionDependence,
    user: UserDependence,
) -> SpinCreateResponse:
    spin = await create_spin(session, user)
    await send_prize_message(
        telegram_id=user.telegram_id,
        prize_name=spin.prize.name,
    )
    post_spin_message = await get_post_spin_message(session)
    if post_spin_message is not None:
        await send_message(
            telegram_id=user.telegram_id,
            text=post_spin_message,
        )

    return SpinCreateResponse(
        spin_id=spin.id,
        prize=PrizeRead.model_validate(spin.prize),
    )
