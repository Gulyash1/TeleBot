from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from datetime import date


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Обслуживание', callback_data='maintance')],
                                     [KeyboardButton(text='Расход')],
                                     [KeyboardButton(text='Запчасти')]],
                           resize_keyboard=True,
                           input_field_placeholder='Пункты меню...',
                           one_time_keyboard=True)

tech = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записать', callback_data='write')],
    [InlineKeyboardButton(text='Последнее', callback_data='last')],
    [InlineKeyboardButton(text='Вся история', callback_data='history')]
])

expend = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записать', callback_data='write_benz')],
    [InlineKeyboardButton(text='Текущий', callback_data='current')]
])
pick_date = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сегодня', callback_data='today')],
    [InlineKeyboardButton(text='Не сегодня', callback_data='not_today')]
])
set_mark = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='mark_yes')],
    [InlineKeyboardButton(text='Нет', callback_data='mark_no')]
])


back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='На главную')]],
                           resize_keyboard=True)

