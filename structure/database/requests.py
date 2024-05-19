import datetime

from structure.database.models import async_session
from structure.database.models import User, TO, Exp
from sqlalchemy import select

async def reg_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def reg_maintance(data):
    async with async_session() as session:
        session.add(TO(date=data['Date'],mileage=data['mileage'], description=data['description']))
        await session.commit()