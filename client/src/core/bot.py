from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault

from src.core.config import settings

bot: Bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)

dp: Dispatcher = Dispatcher()


async def set_bot_commands() -> None:
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота",
        ),
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )
