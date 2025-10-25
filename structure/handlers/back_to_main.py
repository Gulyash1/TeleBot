from aiogram import Router, F
from aiogram.types import CallbackQuery
import structure.keyboards as key

rt_to_main = Router()

@rt_to_main.callback_query(F.data == 'main')
async def main_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=key.main)