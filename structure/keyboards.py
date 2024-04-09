from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ТО')],
                                     [KeyboardButton(text='Расход')],
                                     [KeyboardButton(text='Запчасти')]],
                           resize_keyboard=True,
                           input_field_placeholder='Пункты меню...')
