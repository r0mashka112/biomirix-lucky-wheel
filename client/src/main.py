import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request

from aiogram.types import Update

from src.core.config import settings

from src.core.bot import dp
from src.core.bot import bot
from src.core.bot import set_bot_commands

from src.handlers.start import router as start_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")

    dp.include_routers(
        start_router,
    )

    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    await set_bot_commands()

    logging.info(f"Webhook set to {settings.WEBHOOK_URL}")
    yield

    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")

    update = Update.model_validate(
        await request.json(),
        context={"bot": bot},
    )

    await dp.feed_update(bot, update)

    logging.info("Update processed")
