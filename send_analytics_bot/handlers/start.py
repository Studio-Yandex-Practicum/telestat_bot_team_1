from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


authorized_users = [248393066,]

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    if message.from_user.id in authorized_users:
        await message.answer("Бот готов к формированию отчётов.")
    else:
        await message.answer("К сожалению, у вас нет прав доступа.")
