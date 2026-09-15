from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.app_settings import AppSettings


def normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized_value = value.strip()
    if not normalized_value:
        return None

    return normalized_value


async def get_app_settings(session: AsyncSession) -> AppSettings | None:
    return await session.scalar(
        select(AppSettings).order_by(AppSettings.id).limit(1)
    )


async def get_greeting_message(session: AsyncSession) -> str | None:
    app_settings = await get_app_settings(session)
    if app_settings is None:
        return None

    return normalize_optional_text(app_settings.greeting_message)


async def get_post_spin_message(session: AsyncSession) -> str | None:
    app_settings = await get_app_settings(session)
    if app_settings is None:
        return None

    return normalize_optional_text(app_settings.post_spin_message)
