from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обслуживание', callback_data='maintance')],
    [InlineKeyboardButton(text='Расход', callback_data='consumption')],
    [InlineKeyboardButton(text='Запчасти', callback_data='parts')]
])

tech = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записать', callback_data='write_maintance')],
    [InlineKeyboardButton(text='Последнее', callback_data='get_last_maintance')],
    [InlineKeyboardButton(text='Вся история', callback_data='get_all_history')],
    [InlineKeyboardButton(text='На главную', callback_data='main')]
])

expend = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записать', callback_data='write_consumption')],
    [InlineKeyboardButton(text='Последний', callback_data='get_last_consumption')],
    [InlineKeyboardButton(text='Вся история', callback_data='get_all_consumption_history')],
    [InlineKeyboardButton(text='На главную', callback_data='main')]
])
pick_date = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сегодня', callback_data='today')],
    [InlineKeyboardButton(text='Не сегодня', callback_data='not_today')]
])
set_mark = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='mark_yes')],
    [InlineKeyboardButton(text='Нет', callback_data='mark_no')]
])

