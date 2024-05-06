import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import start, report
#from core.config import settings

load_dotenv()
logging.basicConfig(level=logging.INFO)

table_name = 'Тест таблица для проекта'


async def main():
    #bot = Bot(token=settings.bot_token)
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(start.router, report.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())