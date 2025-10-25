from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message



import structure.keyboards as key
import structure.database.repository as req

rt = Router()

@rt.message(CommandStart())
async def start(msg: Message) -> None:
    await req.reg_user(msg.from_user.id)
    await msg.answer('Давно тебя не было в уличных гонках!')
    await msg.answer_sticker('CAACAgIAAxkBAAMvZhVtcsXyCrc98dR30x31dM8T9e0AAu4nAAJ1vfFLsnWlCwQaDmE0BA')
    await msg.answer("Выберите действие",reply_markup=key.main)


