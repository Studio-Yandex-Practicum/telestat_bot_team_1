import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user_channel import channel_router
from handlers.admin_private import admin_router

from common.bot_cmds_list import private

logging.basicConfig(level=logging.INFO)

ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)

bot.my_admins_list = []  # список администраторов
bot.current_channel = []  # текущий выбранный канал
bot.choice_interval = []  # выбранный интервал опроса

bot.my_admins_list.append(int(os.getenv('SUPERUSER')))  # В .env внесен id суперпользователя

print(bot.my_admins_list)

dp = Dispatcher()

dp.include_routers(channel_router, admin_router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()
    print('Бот работает')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')
