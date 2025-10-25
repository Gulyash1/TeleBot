from datetime import date, datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
import structure.keyboards as key
import structure.database.repository as req
from structure.utils import format_maintance_list
router = Router()


class maintance(StatesGroup):
    data = State()
    mark = State()
    Date = State()

@router.callback_query(F.data == 'maintance')
async def maintance_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=key.tech)
    await callback.answer()

@router.callback_query(F.data == 'write_maintance')
async def write_maintance_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(maintance.data)
    await callback.answer('Ввод данных')

@router.message(maintance.data)
async def maintance_data_callback(msg: Message, state: FSMContext):
    lines = msg.text.split('\n')
    mileage, description = lines
    mileage = int(mileage.strip())
    await state.update_data(mileage=mileage, description=description)
    await state.set_state(maintance.mark)
    await msg.answer('Поставить отметку?', reply_markup=key.set_mark)

@router.callback_query(maintance.mark)
async def maintance_mark_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(mark=callback.data)
    await state.set_state(maintance.Date)
    #await callback.answer('Дата', reply_markup=key.pick_date)
    await callback.message.edit_text('Дата', reply_markup=key.pick_date)

@router.callback_query(F.data == 'today')
async def today_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(Date=date.today())
    data = await state.get_data()
    await save_maintance(callback.message, data)
    await state.clear()



@router.callback_query(F.data == 'not_today')
async def not_today_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Дата в формате ДД.ММ.ГГ')


@router.message(maintance.Date)
async def final_callback(msg: Message, state: FSMContext):
    try:
        parsed_date = datetime.strptime(msg.text.strip(), "%d.%m.%y").date()
        await state.update_data(Date=parsed_date)

        data = await state.get_data()
        await save_maintance(msg, data)
    except ValueError:
        await msg.answer('Дата в формате ДД.ММ.ГГ')
    await state.clear()


async def save_maintance(target, data: dict):
    try:
        success = await req.reg_maintance(data)
        if success:
            await target.answer(
                f"Запись добавлена:\n"
                f"Пробег: {data['mileage']} км\n"
                f"Дата: {data['Date'].strftime('%d.%m.%Y')}\n"
                f"Описание: {data['description']}",
                reply_markup=key.main
            )
        else:
            await target.answer("Не удалось сохранить запись.\n ", reply_markup=key.main)
    except Exception as e:
        await target.answer(f"Произошла ошибка при сохранении.\n {e}", reply_markup=key.main)



@router.callback_query(F.data == 'get_last_maintance')
async def get_last_maintance(callback: CallbackQuery):
    items = await req.get_last_maintance()
    if not items:
        await callback.message.answer('История пуста')
        return
    formated_date = items.date.strftime('%d.%m.%Y')
    msg = f'*Последнее ТО*:\n*Дата:*\n{formated_date}\n*Пробег:*\n{items.mileage}км \n*Описание:*\n{items.description}'
    await callback.message.answer(msg, parse_mode='Markdown', reply_markup=key.main)


@router.callback_query(F.data == 'get_all_history')
async def get_all_maintance_history(callback: CallbackQuery):
    items = await req.get_all_maintance()
    if not items:
        await callback.message.answer('История пуста')
        return
    msg = format_maintance_list(items)
    await callback.message.answer(msg, parse_mode='HTML', reply_markup=key.main)
