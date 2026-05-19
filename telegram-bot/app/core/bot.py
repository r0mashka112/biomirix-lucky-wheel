from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.core.config import settings

bot: Bot = Bot(
    token = settings.BOT_TOKEN
)

dp: Dispatcher = Dispatcher()

async def set_bot_commands() -> None:
    commands = [
        BotCommand(
            command = 'start',
            description = 'Запустить бота'
        )
    ]

    await bot.set_my_commands(
        commands = commands,
        scope = BotCommandScopeDefault()
    )