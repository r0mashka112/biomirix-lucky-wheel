from aiogram.types import InlineKeyboardMarkup
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.config import settings


CHECK_SUBSCRIPTION_CALLBACK_DATA = "check_subscription"


def create_mini_app_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder().button(
        text="Запустить колесо фортуны",
        web_app=WebAppInfo(url=settings.BASE_URL),
    ).as_markup()


def create_subscription_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подписаться на канал",
        url=settings.TELEGRAM_CHANNEL_URL,
    )
    builder.button(
        text="Я подписался",
        callback_data=CHECK_SUBSCRIPTION_CALLBACK_DATA,
    )
    builder.adjust(1)
    return builder.as_markup()
