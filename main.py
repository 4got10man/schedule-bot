import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db.engine import async_session, create_db_and_tables
from handlers import schedule_router, start_router, updates_router
from middlewares import DatabaseMiddleware
from utils import schedule_daily_notifications, scheduler

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.update.middleware(DatabaseMiddleware())
dp.include_routers(start_router, schedule_router, updates_router)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await create_db_and_tables()
    scheduler.start()

    async with async_session() as session:
        await schedule_daily_notifications(session, bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped (KeyboardInterrupt)")
