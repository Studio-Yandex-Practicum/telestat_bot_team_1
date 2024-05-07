from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from send_analytics_bot.services.spreadsheet_manager import google_sheets_manager


router = Router()


@router.message(Command('report'))
async def start(message: Message):
    await message.answer(
        f'Группа в телеграм: {google_sheets_manager.get_table_name()}\n'
        f'Количество подписчиков текущее: '
        f'{google_sheets_manager.get_len_subscribers()}'
    )
