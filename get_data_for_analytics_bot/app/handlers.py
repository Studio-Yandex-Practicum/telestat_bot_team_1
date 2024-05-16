import os
import asyncio
from aiogoogle import Aiogoogle
from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

import app.keyboards as kb
from app.google_table import collect_analytics

router = Router()
load_dotenv()
user1 = os.getenv('USER1')
authorized_users = [4178867722, 5877825258, 1598142492, user1]


@router.message(CommandStart())
async def cmd_start(message: Message):

    if message.from_user.id in authorized_users:
        await message.answer('Нажмите кнопку, чтобы бот собрал аналитику',
                             reply_markup=kb.button)
    else:
        await message.answer('К сожалению, у вас нет прав доступа')


@router.callback_query(F.data == 'collect_analytics')
async def collect_analytics_bot(callback: types.CallbackQuery):
    await callback.message.answer(await collect_analytics())
    await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )
