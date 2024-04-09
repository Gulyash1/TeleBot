from aiogram import Bot, Dispatcher, types, F
import asyncio
from dotenv import load_dotenv
import os
from structure.handlers import rt
load_dotenv()


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Goodbye!')
