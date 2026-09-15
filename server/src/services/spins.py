import random

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.prize import Prize
from src.models.spin import Spin
from src.models.user import User
from src.services.exceptions import ConflictError


async def get_user_spin(
    session: AsyncSession,
    user: User,
) -> Spin | None:
    return await session.scalar(
        select(Spin)
        .where(Spin.user_id == user.id)
        .options(selectinload(Spin.prize))
    )


async def has_available_prizes(session: AsyncSession) -> bool:
    prize_id = await session.scalar(
        select(Prize.id)
        .where(
            Prize.is_active.is_(True),
            Prize.quantity > 0,
        )
        .limit(1)
    )
    return prize_id is not None


async def get_spin_status(
    session: AsyncSession,
    user: User,
) -> tuple[bool, str | None, Spin | None]:
    spin = await get_user_spin(session, user)
    if spin is not None:
        return False, "already_spun", spin

    if not await has_available_prizes(session):
        return False, "no_prizes_left", None

    return True, None, None


async def create_spin(session: AsyncSession, user: User) -> Spin:
    existing_spin = await get_user_spin(session, user)
    if existing_spin is not None:
        raise ConflictError("already_spun")

    while True:
        available_ids = list(
            await session.scalars(
                select(Prize.id)
                .where(
                    Prize.is_active.is_(True),
                    Prize.quantity > 0,
                )
            )
        )

        if not available_ids:
            raise ConflictError("no_prizes_left")

        selected_id = random.choice(available_ids)
        prize = await session.scalar(
            select(Prize)
            .where(Prize.id == selected_id)
            .with_for_update()
        )

        if prize is None or prize.quantity <= 0:
            continue

        prize.quantity -= 1
        spin = Spin(
            user=user,
            prize=prize,
        )
        session.add(spin)

        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise ConflictError("already_spun") from exc

        await session.refresh(spin)
        spin.prize = prize
        return spin
