# import os
#
# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message
# from dotenv import load_dotenv
#
# from send_analytics_bot.handlers.report import report
# from send_analytics_bot.keyboards.start_keyboard import start_keyboard
#
# load_dotenv()
# me = int(os.getenv('ME'))
# authorized_users = [me,]
#
# router = Router()
#
#
# @router.message(Command('start'))
# async def start(message: Message):
#     if message.from_user.id not in authorized_users:
#         await message.answer('К сожалению, у вас нет прав доступа.')
#     await message.answer(
#         'Бот готов к формированию отчетов.', reply_markup=start_keyboard())
#
#
# @router.message()
# async def on_report_command(message: Message):
#     if message.text == 'Сформировать отчет':
#         await report(message)
