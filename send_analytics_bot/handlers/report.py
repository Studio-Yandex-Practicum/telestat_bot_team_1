from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command('report'))
async def start(message: Message):
    await message.answer("Напишите название канала")