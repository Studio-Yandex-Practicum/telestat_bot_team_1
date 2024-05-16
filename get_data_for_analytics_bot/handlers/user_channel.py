from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_channel, orm_delete_channel, orm_get_channel
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from handlers.admin_private import ADMIN_KB

channel_router = Router()
channel_router.message.filter(ChatTypeFilter(['channel']), IsAdmin())

channel_router = Router()


@channel_router.channel_post(Command(commands=['add']))
async def channel_post_handler(channel_post: types.Message, session: AsyncSession):
    data = {'channel_id': channel_post.chat.id, 'channel_name': channel_post.chat.title}
    try:
        for channel_id in await orm_get_channel(session):
            if channel_id.channel_id == channel_post.chat.id:
                await channel_post.answer(f'Канал {channel_id.channel_name}, уже добавлен в базу данных!')
                return
        await orm_add_channel(session, data)
        await channel_post.answer(
            f'Канал  {str(channel_post.chat.title)}, добавлен в базу данных!!')

    except Exception as e:
        await channel_post.answer(
            f'Ошибка: \n{str(e)}\nОбратись к программисту!',
        )


@channel_router.channel_post(Command(commands=['del']))
async def del_channel_name(channel_post: types.Message, session: AsyncSession):
    for channel_id in await orm_get_channel(session):
        print(f'channel_id.channel_id = {channel_id.channel_id}')
        print(f'channel_post.chat.id = {channel_post.chat.id}')

        if channel_id.channel_id == channel_post.chat.id:
            await orm_delete_channel(session, channel_id.channel_id)
            await channel_post.answer(
                f'Канал  {str(channel_id.channel_id)}, удален из базы данных!!')
            return

    await channel_post.answer('Вы не можете удалить канал, он еще не добавлен в базу данных!!')

