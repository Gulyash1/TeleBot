import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BotCommand
from dotenv import load_dotenv

from structure.handlers import rt
from structure.database.models import db_main
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("telebot")


async def bot_main() -> None:
    logger.info("Initializing database...")
    await db_main()
    logger.info("Database initialized")

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(rt)

    logger.info("Starting bot polling")
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        logger.info('Goodbye!')
