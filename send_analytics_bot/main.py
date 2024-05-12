import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import start, report


load_dotenv()
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(start.router, report.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
