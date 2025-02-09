from sqlalchemy import select,update
from app.database.models import User,async_session
from typing import Optional

#TG_ID.
async def set_datas(tg_id:int, full_name:str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, full_name=full_name)
            session.add(new_user)
            await session.commit()

async def get_id(tg_id:int)-> None:
    async with async_session() as session:
        return await session.scalar(select(User.tg_id).where(User.tg_id == tg_id))
    
#GROUPS.
async def set_group(tg_id:int, group:str) -> None:
    async with async_session() as session:
        group = await session.execute(update(User).where(User.tg_id == tg_id).values(group=group))

        if group.rowcount == 0:
            new_group = User(tg_id=tg_id, group=group)
            session.add(new_group)
            
        await session.commit()

async def get_group(tg_id:int) -> Optional[str]:
    async with async_session() as session:
        return await session.scalar(select(User.group).where(User.tg_id == tg_id))
    