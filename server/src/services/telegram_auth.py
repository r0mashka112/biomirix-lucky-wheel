import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from urllib.parse import parse_qsl

from src.core.config import settings
from src.services.exceptions import UnauthorizedError


@dataclass(frozen=True)
class TelegramInitDataUser:
    telegram_id: int
    username: str | None


def validate_telegram_init_data(init_data: str) -> TelegramInitDataUser:
    parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed_data.pop("hash", None)
    if received_hash is None:
        raise UnauthorizedError("invalid_init_data")

    data_check_string = "\n".join(
        f"{key}={value}"
        for key, value in sorted(parsed_data.items())
    )
    secret_key = hmac.new(
        b"WebAppData",
        settings.BOT_TOKEN.get_secret_value().encode(),
        hashlib.sha256,
    ).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise UnauthorizedError("invalid_init_data")

    auth_date_value = parsed_data.get("auth_date")
    if auth_date_value is None:
        raise UnauthorizedError("invalid_init_data")

    try:
        auth_date = datetime.fromtimestamp(int(auth_date_value), tz=UTC)
    except ValueError as exc:
        raise UnauthorizedError("invalid_init_data") from exc

    now = datetime.now(tz=UTC)
    max_age_seconds = settings.TELEGRAM_INIT_DATA_MAX_AGE_SECONDS
    if (now - auth_date).total_seconds() > max_age_seconds:
        raise UnauthorizedError("expired_init_data")

    user_json = parsed_data.get("user")
    if user_json is None:
        raise UnauthorizedError("invalid_init_data")

    try:
        user_data = json.loads(user_json)
        telegram_id = int(user_data["id"])
    except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise UnauthorizedError("invalid_init_data") from exc

    username = user_data.get("username")
    if username is not None:
        username = str(username)

    return TelegramInitDataUser(
        telegram_id=telegram_id,
        username=username,
    )
