from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import structure.keyboards as key
import structure.database.requests as req
from structure.utils import format_maintance_list
import logging

from datetime import date
rt = Router()

logger = logging.getLogger(__name__)

class Write_mileage(StatesGroup):
    mileage = State()
    description = State()
    Date = State()
    Mark = State()

@rt.message(CommandStart())
async def start(msg: Message) -> None:
    await req.reg_user(msg.from_user.id)
    await msg.answer('Давно тебя не было в уличных гонках!')
    await msg.answer_sticker('CAACAgIAAxkBAAMvZhVtcsXyCrc98dR30x31dM8T9e0AAu4nAAJ1vfFLsnWlCwQaDmE0BA', reply_markup=key.main)


@rt.message(F.text == 'Обслуживание')
async def TOs(msg: Message) -> None:
    logger.info("Выбор для обслуживания")
    await msg.answer('Выберите действие',reply_markup=key.tech)

@rt.message(F.text == 'Расход')
async def exp(msg: Message) -> None:
    await msg.answer('Выберите действие', reply_markup=key.expend)

@rt.callback_query(F.data == 'write')
async def write_callback(msg: Message, state: FSMContext) -> None:
    logger.info("Ввод пробега")
    await state.set_state(Write_mileage.mileage)
    await msg.answer('Ввести пробег')
@rt.message(Write_mileage.mileage)
async def mileage_callback(msg: Message, state:FSMContext):
    logger.info("Описание")
    await state.update_data(mileage=msg.text)
    await state.set_state(Write_mileage.description)
    await msg.answer('Что было сделано?')

@rt.message(Write_mileage.description)
async def description_callback(msg: Message, state: FSMContext):
    logger.info("Дата")
    await state.update_data(description=msg.text)
    await state.set_state(Write_mileage.Mark)
    await msg.answer('Поставить отметку?', reply_markup=key.set_mark)


@rt.callback_query(Write_mileage.Mark)
async def mark_callback(callback: CallbackQuery, state: FSMContext):
    logger.info("Mark")
    await state.update_data(Mark=callback.data)
    await state.set_state(Write_mileage.Date)
    await callback.message.answer('Дата', reply_markup=key.pick_date)
    await callback.answer()

@rt.callback_query(F.data == 'today')
async def today_callback(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        logger.info(f"Creating maintenance record with data: {data}")
        
        # Ensure we have all required fields
        if not all(key in data for key in ['mileage', 'description']):
            await callback.message.answer("Ошибка: Недостаточно данных для сохранения")
            return
            
        # Add today's date
        data['Date'] = date.today()
        
        # Try to save the record
        success = await req.reg_maintance(data)
        if success:
            await callback.message.answer(
                f"✅ Запись добавлена\n"
                f"Пробег: {data['mileage']}\n"
                f"Описание: {data['description']}\n"
                f"Дата: {data['Date'].strftime('%d.%m.%Y')}"
            )
        else:
            await callback.message.answer("❌ Не удалось сохранить запись. Попробуйте снова.")
            
    except Exception as e:
        logger.error(f"Error in today_callback: {str(e)}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при сохранении. Пожалуйста, попробуйте снова.")
    finally:
        await state.clear()

@rt.callback_query(F.data == 'not_today')
async def not_today_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Дата')

@rt.message(Write_mileage.Date)
async def final_callback(msg: Message, state: FSMContext):
    await state.update_data(Date=msg.text)
    data = await state.get_data()
    logger.info(f"Custom date {data['Date']}")
    await msg.answer(f"Пробег: {data['mileage']}\nОписание: {data['description']}\nДата: {data['Date']}\n")
    await req.reg_maintance(data)
    await state.clear()


@rt.callback_query(F.data == 'last')
async def get_last(callback: CallbackQuery):
    items = await req.get_all_maintance(latest=True)
    if not items:
        await callback.message.answer('История пуста')
        return
    formated_date = items.date.strftime('%d.%m.%Y')
    msg = f'*Последнее ТО*:\n*Дата:*\n{formated_date}\n*Пробег:*\n{items.mileage}км \n*Описание:*\n{items.description}'
    await callback.message.answer(msg, parse_mode='Markdown')

@rt.callback_query(F.data == 'history')
async def get_history(callback: CallbackQuery):
    logger.info("Вызов истории")
    items = await req.get_all_maintance()
    if not items:
        logger.info("Возвращаем пустую историю")
        await callback.message.answer('История пуста')
        return
    msg = format_maintance_list(items)
    await callback.message.answer(msg, parse_mode='HTML')

