from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.core.config import settings
from app.utils.event_helper import get_event_or_reply
from app.middlewares.subscription import check_subscription

from app.keyboards.web_app import create_mini_app_keyboard
from app.keyboards.subscription import create_subscribe_keyboard

router: Router = Router()

@router.message(Command('start'))
@check_subscription(chat_id = settings.CHAT_ID)
async def handle_start(
    message: Message,
    is_subscribed: bool
) -> None:
    if not is_subscribed:
        await message.answer(
            text = settings.MESSAGE_IF_NOT_SUBSCRIBED,
            reply_markup = create_subscribe_keyboard(),
            parse_mode = 'HTML'
        )

        return

    event = await get_event_or_reply(message)

    if not event:
        return

    await message.answer(
        text = event.get('welcomeText') or settings.GREETING_MESSAGE,
        parse_mode = 'HTML'
    )

    await message.answer(
        text = settings.MESSAGE_IF_SUBSCRIBED,
        reply_markup = create_mini_app_keyboard()
    )