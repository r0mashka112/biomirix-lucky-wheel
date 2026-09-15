from fastapi import APIRouter

from src.api.deps import UserDependence
from src.deps import SessionDependence
from src.schemas.prize import PrizeRead
from src.schemas.spin import SpinRead
from src.schemas.spin import SpinStatusRead
from src.schemas.user import UserRead
from src.services.spins import get_spin_status

router = APIRouter()


@router.get("", response_model=UserRead)
async def get_me(user: UserDependence) -> UserRead:
    return UserRead.model_validate(user)


@router.get("/spin-status", response_model=SpinStatusRead)
async def get_me_spin_status(
    session: SessionDependence,
    user: UserDependence,
) -> SpinStatusRead:
    can_spin, reason, spin = await get_spin_status(session, user)

    spin_read = None
    if spin is not None:
        spin_read = SpinRead(
            id=spin.id,
            prize=PrizeRead.model_validate(spin.prize),
        )

    return SpinStatusRead(
        can_spin=can_spin,
        reason=reason,
        spin=spin_read,
    )
