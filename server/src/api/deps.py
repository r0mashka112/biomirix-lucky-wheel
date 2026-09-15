from typing import Annotated

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from src.deps import SessionDependence
from src.models.user import User
from src.services.telegram_auth import validate_telegram_init_data
from src.services.users import get_or_create_user


async def get_user(
    session: SessionDependence,
    x_telegram_init_data: Annotated[str | None, Header()] = None,
) -> User:
    if x_telegram_init_data is None:
        raise HTTPException(
            status_code=401,
            detail={"reason": "missing_init_data"},
        )

    telegram_user = validate_telegram_init_data(x_telegram_init_data)
    return await get_or_create_user(
        session,
        telegram_id=telegram_user.telegram_id,
        username=telegram_user.username,
    )


UserDependence = Annotated[User, Depends(get_user)]
