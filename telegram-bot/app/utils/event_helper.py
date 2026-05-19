from aiogram.types import (
    Message,
    CallbackQuery
)

from app.services.backend_api import BackendAPI

async def get_event_or_reply(
    target: Message | CallbackQuery
):
    result = await BackendAPI.get_event()

    if result['success']:
        return result['data']

    text = 'Произошла ошибка'

    if result['code'] == 'EVENT_NOT_FOUND':
        text = 'В данный момент нет розыгрышей'

    if isinstance(target, CallbackQuery):
        await target.message.answer(text = text)
    else:
        await target.answer(text = text)

    return None