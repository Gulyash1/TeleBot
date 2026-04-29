import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from structure.handlers import all_routers

from structure.database.session import init_models
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

console = logging.StreamHandler()
handler = RotatingFileHandler(
    "logs/bot.log",
    maxBytes=10_000_000,
    backupCount=5
)

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[handler, console],
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger("telebot")

async def bot_main() -> None:
    logger.info("Initializing database...")
    await init_models()
    logger.info("Database initialized")

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    for rt in all_routers:
        dp.include_router(rt)

    logger.info("Starting bot polling")
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(bot_main())
    except Exception as e:
        logging.exception("FATAL ERROR")
        raise