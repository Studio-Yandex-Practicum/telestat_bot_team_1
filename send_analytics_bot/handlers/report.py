from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from send_analytics_bot.keyboards.report_keyboard import report_keyboard
from send_analytics_bot.services.format_manager import format_manager

router = Router()


@router.message(Command('report'))
async def report(message: Message):
    await message.answer(
        'Выберите формат отчета:',
        reply_markup=report_keyboard()
    )


@router.callback_query()
async def on_callback_query(callback_query: types.CallbackQuery):
    format_selection = callback_query.data
    if format_selection == 'report_msg':
        await callback_query.message.answer(format_manager.message())
    else:
        document = FSInputFile(
            format_manager.format_selection(format_selection))
        await callback_query.message.answer_document(document)
    await callback_query.message.delete()

    await callback_query.answer()
