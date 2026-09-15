from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError
from aiogram import F

from src.core.bot import bot
from src.core.config import settings
from src.keyboards.web_app import CHECK_SUBSCRIPTION_CALLBACK_DATA
from src.keyboards.web_app import create_mini_app_keyboard
from src.keyboards.web_app import create_subscription_keyboard
from src.services.backend import get_greeting_message

router: Router = Router()


SUBSCRIBED_STATUSES = {
    ChatMemberStatus.CREATOR,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
}


async def is_user_subscribed(user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(
            chat_id=settings.TELEGRAM_CHANNEL_ID,
            user_id=user_id,
        )
    except TelegramAPIError:
        return False

    return chat_member.status in SUBSCRIBED_STATUSES


async def send_subscription_state(message: Message) -> None:
    if message.from_user is None:
        await message.answer(settings.MESSAGE_IF_NOT_UNDERSTAND)
        return

    greeting_message = await get_greeting_message()
    await message.answer(greeting_message or settings.GREETING_MESSAGE)

    if await is_user_subscribed(message.from_user.id):
        await message.answer(
            settings.MESSAGE_IF_SUBSCRIBED,
            reply_markup=create_mini_app_keyboard(),
        )
        return

    await message.answer(
        settings.MESSAGE_IF_NOT_SUBSCRIBED,
        reply_markup=create_subscription_keyboard(),
    )


@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    await send_subscription_state(message)


@router.callback_query(F.data == CHECK_SUBSCRIPTION_CALLBACK_DATA)
async def handle_check_subscription(callback: CallbackQuery) -> None:
    if callback.from_user is None or not isinstance(callback.message, Message):
        await callback.answer()
        return

    if await is_user_subscribed(callback.from_user.id):
        await callback.message.answer(
            settings.MESSAGE_IF_SUBSCRIBED,
            reply_markup=create_mini_app_keyboard(),
        )
        await callback.answer()
        return

    await callback.message.answer(
        settings.MESSAGE_IF_NOT_SUBSCRIBED,
        reply_markup=create_subscription_keyboard(),
    )
    await callback.answer("Подписка пока не найдена")


@router.message()
async def handle_unknown_message(message: Message) -> None:
    await message.answer(settings.MESSAGE_IF_NOT_UNDERSTAND)
