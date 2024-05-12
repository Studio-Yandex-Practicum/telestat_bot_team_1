import os
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from datetime import datetime
from dotenv import load_dotenv

import app.keyboards as kb
from app.keyboards import command
from app.parser import parser

router = Router()
load_dotenv()
user1 = os.getenv('USER1')


@router.message(CommandStart())
async def cmd_start(message: Message):
    authorized_users = [4178867722, 5877825258, user1]
    if message.from_user.id in authorized_users:
        await message.answer('Hello', reply_markup=kb.button)
    else:
        await message.answer('К сожалению, у вас нет прав доступа')


@router.callback_query_handler(command.filter(function='parser'))
async def parser_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    try:
        parser.run()
    except KeyboardInterrupt:
        finish = datetime.today().strftime('%m/%d/%y %H:%M')
        print(f'App finished at{finish}')
