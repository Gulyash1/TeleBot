from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command

import structure.keyboards as key

rt = Router()


@rt.message(CommandStart())
async def start(msg: types.Message) -> None:
    await msg.answer('Hi!')
    await msg.answer_sticker('CAACAgIAAxkBAAMvZhVtcsXyCrc98dR30x31dM8T9e0AAu4nAAJ1vfFLsnWlCwQaDmE0BA', reply_markup=key.main)
@rt.message(F.content_type.in_({'sticker'}))
async def echo(mesagge: types.Message) -> None:
    await mesagge.answer(mesagge.sticker.file_id)
