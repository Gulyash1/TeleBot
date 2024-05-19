import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BotCommand
from dotenv import load_dotenv
import os

from structure.handlers import rt
from structure.database.models import db_main
load_dotenv()


async def bot_main() -> None:
    await db_main()

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(rt)

    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print('Goodbye!')
