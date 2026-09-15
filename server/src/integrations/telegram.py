import json
import logging
from html import escape
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

import anyio

from src.core.config import settings

logger = logging.getLogger(__name__)


def _send_message_sync(chat_id: int, text: str) -> None:
    bot_token = settings.BOT_TOKEN.get_secret_value()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
    ).encode("utf-8")
    request = Request(
        url=url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        response_body = json.loads(response.read().decode("utf-8"))

    if not response_body.get("ok"):
        raise RuntimeError(f"Telegram API returned unsuccessful response: {response_body}")


async def send_message(
    *,
    telegram_id: int,
    text: str,
) -> None:
    try:
        await anyio.to_thread.run_sync(
            _send_message_sync,
            telegram_id,
            text,
        )
    except (HTTPError, URLError, OSError, RuntimeError, json.JSONDecodeError):
        logger.exception(
            "Failed to send Telegram message to user %s",
            telegram_id,
        )


async def send_prize_message(
    *,
    telegram_id: int,
    prize_name: str,
) -> None:
    text = f"Поздравляем! Ваш приз: <b>{escape(prize_name)}</b>"
    await send_message(
        telegram_id=telegram_id,
        text=text,
    )
