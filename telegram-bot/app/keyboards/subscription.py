from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_subscribe_keyboard() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder()
        .button(
            text = 'Подписаться',
            url = 'https://t.me/biomirix'
        ).button(
            text = 'Начать розыгрыш',
            callback_data = 'start_raffle'
        )
        .adjust(1)
        .as_markup()
    )