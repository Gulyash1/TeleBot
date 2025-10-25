from datetime import date

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import structure.keyboards as key
from structure.utils import format_consumption_list
from structure.database import repository as req

consumption_router = Router()

class consumption(StatesGroup):
    Data = State()



@consumption_router.callback_query(F.data == 'consumption')
async def write_consumption_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=key.expend)
    await callback.answer()

@consumption_router.callback_query(F.data == 'write_consumption')
async def write_consumption_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(consumption.Data)
    await callback.answer('Введите данные в формате:\nПробег\nЛитры')

@consumption_router.message(consumption.Data)
async def consumption_data_callback(msg: Message, state: FSMContext):
    lines = msg.text.split('\n')
    mileage, liters = lines
    mileage = int(mileage.strip())

    if mileage > 1000:
        last = await req.get_last_consumption()
        mileage -= last.mileage
    liters = float(liters.strip())
    avg = round((liters / mileage) * 100, 2)
    await state.update_data(mileage=mileage, liters=liters, avg=avg, Date=date.today())
    data = await state.get_data()
    await save_consumption(msg, data)
    await state.clear()

@consumption_router.callback_query(F.data == 'get_last_consumption')
async def get_last(callback: CallbackQuery):
    items = await req.get_last_consumption()
    if not items:
        await callback.message.answer('История пуста')
        return
    msg = (f'*Пробег:*{items.mileage}км'
           f'\n*Литры:*{items.liters}л'
           f'\n*Средний расход:*{items.mean}л/100км')
    await callback.message.answer(msg, parse_mode='Markdown', reply_markup=key.main)

@consumption_router.callback_query(F.data == 'get_all_consumption_history')
async def get_all_consumption_history(callback: CallbackQuery):
    items = await req.get_all_consumption()
    if not items:
        await callback.message.answer('История пуста')
        return
    msg = format_consumption_list(items)
    await callback.message.answer(msg, parse_mode='HTML', reply_markup=key.main)



async def save_consumption(target, data: dict):
    try:
        success = await req.reg_consumption(data)
        if success:
            await target.answer(
                f"Запись добавлена:\n"
                f"Пробег: {data['mileage']} км\n"
                f"Литры: {data['liters']}л\n"
                f"Средний расход: {data['avg']}л/100км\n"
                f"Дата: {data['Date'].strftime('%d.%m.%Y')}\n",
                reply_markup=key.main
            )
        else:
            await target.answer("Не удалось сохранить запись.", reply_markup=key.main)
    except Exception as e:
        await target.answer(f"Произошла ошибка при сохранении.\n {e}", reply_markup=key.main)
