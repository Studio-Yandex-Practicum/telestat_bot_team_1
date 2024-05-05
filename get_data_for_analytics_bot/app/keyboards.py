from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


command = CallbackData()
button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='начать сбор аналитики',
        callback_data='parser')]
])

#@dp.callback_query_handler(command.filter(function='test'))
#async def test(query: types.CallbackQuery, callback_data: dict):