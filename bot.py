from aiogram import Bot, Dispatcher, types
import asyncio

from aiogram.filters import CommandStart

bot = Bot(token='7042221074:AAGukPmlTiFIdZeYl0TKxFy6nFON2a866LY')

dp = Dispatcher(bot=bot)


@dp.message(CommandStart())
async def start(msg: types.Message) -> None:
    await msg.answer('Hi!')
@dp.message()
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    #executor.start_polling(dp)
