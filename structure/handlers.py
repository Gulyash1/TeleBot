from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import structure.keyboards as key
import structure.database.requests as req

from datetime import date
rt = Router()



class Write_mileage(StatesGroup):
    mileage = State()
    description = State()
    Date = State()

@rt.message(CommandStart())
async def start(msg: Message) -> None:
    await req.reg_user(msg.from_user.id)
    await msg.answer('Давно тебя не было в уличных гонках!')
    await msg.answer_sticker('CAACAgIAAxkBAAMvZhVtcsXyCrc98dR30x31dM8T9e0AAu4nAAJ1vfFLsnWlCwQaDmE0BA', reply_markup=key.main)


# @rt.callback_query(F.data == 'maintance')
# async def TOs(callback: CallbackQuery) -> None:
#     await callback.message.answer('Выбор', reply_markup=key.tech)
@rt.message(F.text == 'Обслуживание')
async def TOs(msg: Message) -> None:
    await msg.answer('Выберите действие',reply_markup=key.tech)

@rt.message(F.text == 'Расход')
async def exp(msg: Message) -> None:
    await msg.answer('Выберите действие', reply_markup=key.expend)

@rt.callback_query(F.data == 'write')
async def write_callback(msg: Message, state: FSMContext) -> None:
    await state.set_state(Write_mileage.mileage)
    await msg.answer('Ввести пробег')

# @rt.message(Command("writeto"))
# async def write_callback(msg: Message, state: FSMContext) -> None:
#     await state.set_state(Write_mileage.mileage)
#     await msg.answer('Ввести пробег')

@rt.message(Write_mileage.mileage)
async def mileage_callback(msg: Message, state:FSMContext):
    await state.update_data(mileage=msg.text)
    await state.set_state(Write_mileage.description)
    await msg.answer('Что было сделано?')

@rt.message(Write_mileage.description)
async def description_callback(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await state.set_state(Write_mileage.Date)
    await msg.answer('Дата',reply_markup=key.pick_date)


@rt.callback_query(F.data == 'today')
async def today_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(Date=date.today())
    data = await state.get_data()
    print(type(data['Date']), data['Date'])
    await req.reg_maintance(data)
    await callback.message.answer(f'Пробег: {data['mileage']}\nОписание: {data['description']}\nДата: {data['Date']}\n')
    await state.clear()
@rt.callback_query(F.data == 'not_today')
async def not_today_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите дату')

@rt.message(Write_mileage.Date)
async def final_callback(msg: Message, state: FSMContext):
    await state.update_data(Date=msg.text)
    data = await state.get_data()
    await msg.answer(f'Пробег: {data['mileage']}\nОписание: {data['description']}\nДата: {data['Date']}\n')
    await req.reg_maintance(data)
    await state.clear()



# @rt.message(BotCommand == 'write')
# async def test(msg: Message) -> None:
#     await msg.answer('test')
# @rt.message(Command('write'))
# async def write(msg: Message, state: FSMContext) -> None:
#     await state.set_state(Write_mileage.mileage)
#     await msg.answer('Пробег')
#
# @rt.message(Write_mileage.mileage)
# async def write_description(msg: Message, state: FSMContext):
#     await state.update_data(description=msg)
#     data = await state.get_data()
#     await msg.answer('data')
#     await state.clear()

