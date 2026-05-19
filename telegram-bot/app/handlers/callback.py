from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.core.config import settings
from app.utils.event_helper import get_event_or_reply
from app.middlewares.subscription import check_subscription

from app.keyboards.web_app import create_mini_app_keyboard
from app.keyboards.subscription import create_subscribe_keyboard

router: Router = Router()

@router.callback_query(F.data == 'start_raffle')
@check_subscription(chat_id = settings.CHAT_ID)
async def handle_callback_query(
    callback_query: CallbackQuery,
    is_subscribed: bool
)-> None:
    await callback_query.answer()

    if not is_subscribed:
        await callback_query.message.answer(
            text = settings.MESSAGE_IF_NOT_SUBSCRIBED,
            parse_mode = 'HTML'
        )

        return

    event = await get_event_or_reply(
        callback_query
    )

    if not event:
        return

    await callback_query.message.answer(
        text = event.get('welcomeText') or settings.GREETING_MESSAGE,
        parse_mode = 'HTML'
    )

    await callback_query.message.answer(
        text = settings.MESSAGE_IF_SUBSCRIBED,
        reply_markup = create_mini_app_keyboard()
    )
