from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='начать сбор аналитики',
        callback_data='collect_analytics')]
])
