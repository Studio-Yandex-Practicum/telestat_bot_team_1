from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from send_analytics_bot.services.format_manager import format_manager

router = Router()


@router.message(Command('report'))
async def report(message: Message):
    await message.answer(
        format_manager.message()
    )


@router.message(Command('report_csv'))
async def report_csv(message: Message):
    document = FSInputFile(format_manager.format_selection('.csv'))
    await message.answer_document(document)


@router.message(Command('report_pdf'))
async def pdf(message: Message):
    document = FSInputFile(format_manager.format_selection('.pdf'))
    await message.answer_document(document)


@router.message(Command('report_xlsx'))
async def excel(message: Message):
    document = FSInputFile(format_manager.format_selection('.xlsx'))
    await message.answer_document(document)
