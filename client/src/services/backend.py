import logging

import aiohttp

from src.core.config import settings

logger = logging.getLogger(__name__)


async def get_greeting_message() -> str | None:
    url = f"{settings.BACKEND_API_URL}/settings/public"

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None

                data = await response.json()
    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception("Failed to fetch public settings from backend")
        return None

    greeting_message = data.get("greeting_message")
    if not isinstance(greeting_message, str):
        return None

    greeting_message = greeting_message.strip()
    if not greeting_message:
        return None

    return greeting_message
