from aiogram import Router
from aiogram.types import Message

from app.core.config import settings

router: Router = Router()

@router.message()
async def handle_unknown(message: Message) -> None:
    await message.answer(
        text = settings.MESSAGE_IF_NOT_UNDERSTAND
    )