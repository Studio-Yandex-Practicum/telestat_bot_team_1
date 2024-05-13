from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def report_keyboard():
    buttons = [[
        InlineKeyboardButton(text='PDF', callback_data='.pdf'),
        InlineKeyboardButton(text='Excel', callback_data='.xlsx'),
        InlineKeyboardButton(text='CSV', callback_data='.csv'),
        InlineKeyboardButton(text='Сообщение', callback_data='report_msg')
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
