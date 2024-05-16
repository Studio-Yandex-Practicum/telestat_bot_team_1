from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserTG, ChannelTG, ParsingPROD


async def orm_add_admin(session: AsyncSession, data: dict):
    obj = (UserTG(
        username=data['username'],
        is_admin=True,
    ))
    session.add(obj)
    await session.commit()


async def orm_get_admins(session: AsyncSession):
    query = select(UserTG)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_admin(session: AsyncSession, user_id: int):
    query = delete(UserTG).where(UserTG.id == user_id)
    await session.execute(query)
    await session.commit()


async def orm_add_channel(session: AsyncSession, data: dict):
    obj = ChannelTG(
        channel_id=data['channel_id'],
        channel_name=data['channel_name'],

    )
    session.add(obj)
    await session.commit()


async def orm_delete_channel(session: AsyncSession, channel_id: int):
    query = delete(ChannelTG).where(ChannelTG.channel_id == channel_id)
    await session.execute(query)
    await session.commit()


async def orm_get_channel(session: AsyncSession):
    query = select(ChannelTG)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_period_parsing(session: AsyncSession, data: dict):
    obj = ParsingPROD(
        period_id=data['period_id'],
        period=data['period'],
    )
    session.add(obj)
    await session.commit()


async def orm_update_channel(session: AsyncSession, channel_id: int, data):
    query = (
        update(ChannelTG)
        .where(ChannelTG.id == channel_id)
        .values(
            channel_current=data['channel_current'],

        )
    )
    await session.execute(query)
    await session.commit()

