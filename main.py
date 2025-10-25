import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from structure.handlers.start_handler import rt
from structure.handlers.maintance import router
from structure.handlers.back_to_main import rt_to_main
from structure.handlers.consumption import consumption_router
from structure.database.session import init_models
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("telebot")


async def bot_main() -> None:
    logger.info("Initializing database...")
    await init_models()
    logger.info("Database initialized")

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(rt)
    dp.include_router(router)
    dp.include_router(consumption_router)
    dp.include_router(rt_to_main)


    logger.info("Starting bot polling")
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        logger.info('Goodbye!')
