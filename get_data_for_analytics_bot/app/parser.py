import os
import asyncio
from datetime import datetime
from pyrogram import Client, filters, types
from dotenv import load_dotenv

load_dotenv()

parser = Client('BotParser', api_id=os.getenv('API_ID'),
                api_hash=os.getenv('API_HASH'),
                phone_number=os.getenv('PHONE_NUMBER'),
                bot_token=os.getenv('TOKEN'))
started = datetime.today().strftime('%m/%d/%y %H:%M')
print(f'App started at {started}')


async def parse_chat(target):
    with open(f'{target}.txt', 'w', encoding='utf8') as file:
        i = 0
        async for member in parser.get_chat_members(target):
            i += 1
#          await asyncio.sleep(1)
            print(i, member.user.id,
                  member.user.id,
                  member.user.first_name,
                  member.user.phone_number, file=file)


@parser.on_message(filters.command('parse') & filters.chat('Myhelper'))
async def chat_parser(client, message):
    target_chat = message.text.split()[1].strip()
    await parse_chat(target_chat)


try:
    parser.run()
except KeyboardInterrupt:
    finish = datetime.today().strftime('%m/%d/%y %H:%M')
    print(f'App finished at{finish}')
