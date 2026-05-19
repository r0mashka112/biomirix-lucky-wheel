from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, WebAppInfo

from app.core.config import settings

def create_mini_app_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder().button(
        text = 'Запустить колесо фортуны',
        web_app = WebAppInfo(url = settings.BASE_URL)
    ).as_markup(resize_keyboard = True)