import os
import csv
import asyncio
import pyrogram
from datetime import datetime
from pyrogram import Client, filters, types
from dotenv import load_dotenv

import contstants

load_dotenv()


async def parsing():
    async with pyrogram.Client('my_session', api_id=os.getenv('API_ID'),
                               api_hash=os.getenv('API_HASH'),
                               bot_token=os.getenv('TOKEN'),
                               phone_number=os.getenv('PHONE_NUMBER')
                               ) as client:
        members = client.get_chat_members(os.getenv('TARGET_CHAT'))
        results = []
        async for member in members:
            results.append([member.user.first_name, member.user.id,
                            member.user.username, member.joined_date,
                            member.user.phone_number,
                            member.user.last_online_date])
        with open(contstants.file_path, 'w', encoding='utf8') as f:
            for result in results:
                print(result)
                writer = csv.writer(f, delimiter=' ')
                writer.writerow(result)


try:
    asyncio.run(parsing())
except KeyboardInterrupt:
    finish = datetime.today().strftime('%m/%d/%y %H:%M')
    print(f'App finished at{finish}')
