import uvicorn
import logging
from aiogram.types import Update
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.bot import bot, dp, set_bot_commands

from app.handlers.start import router as start_router
from app.handlers.unknown import router as unknown_router
from app.handlers.callback import router as callback_router

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")

    dp.include_routers(
        start_router,
        callback_router,
        unknown_router
    )

    await bot.set_webhook(
        url = settings.WEBHOOK_URL,
        allowed_updates = dp.resolve_used_update_types(),
        drop_pending_updates = True
    )

    await set_bot_commands()

    logging.info(f"Webhook set to {settings.WEBHOOK_URL}")
    yield

    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Webhook deleted")


app = FastAPI(lifespan = lifespan)

@app.post('/webhook')
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")

    update = Update.model_validate(
        await request.json(),
        context = {'bot': bot}
    )

    await dp.feed_update(bot, update)

    logging.info("Update processed")

if __name__ == '__main__':
    uvicorn.run('main:app', host = '0.0.0.0', port = 8000)