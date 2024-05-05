from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f

from filters.chat_types import ChatTypeFilter
from kbds import reply


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник', reply_markup=reply.start_kb)


@user_private_router.message(or_f(Command('Выбор Telegram-канала'), (F.text.lower() == 'Выбор Telegram-канала')))
async def menu_cmd(message: types.Message):
    await message.answer('Выбор Telegram-канала')


@user_private_router.message(Command('Установка периода сбора данных'))
async def about_cmd(message: types.Message):
    await message.answer('Установка периода сбора данных')


@user_private_router.message(Command('Добавить администратора'))
async def payment_cmd(message: types.Message):
    await message.answer('Удалить администратора')


@user_private_router.message(Command('Удалить администратора'))
async def menu_cmd(message: types.Message):
    await message.answer('Добавить администратора')
