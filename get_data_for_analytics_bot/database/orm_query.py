from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserTG


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
