from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None = None,
) -> User:
    user = await session.scalar(
        select(User).where(User.telegram_id == telegram_id)
    )

    if user is not None:
        if user.username != username:
            user.username = username
            await session.commit()
            await session.refresh(user)
        return user

    user = User(
        telegram_id=telegram_id,
        username=username
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
