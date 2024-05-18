import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# from get_data_for_analytics_bot.database.engine import session_maker
from handlers import adpin_panel

load_dotenv()
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    # dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_routers(
        # start.router,
        # report.router,
        adpin_panel.admin_router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
