from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_keyboard():
    kb = [[KeyboardButton(text="Сформировать отчет")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
