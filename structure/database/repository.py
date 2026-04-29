import datetime
from decimal import Decimal

from structure.database.models import User, TO, Consumption
from structure.database.session import async_session
from sqlalchemy import select
from structure.utils import find_markup_words
import logging


logger = logging.getLogger(__name__)

async def reg_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def reg_maintance(data):
    try:
        async with async_session() as session:
            logger.info(f"Received data for maintenance: {data}")

            if isinstance(data['Date'], str):
                convert_date = datetime.datetime.strptime(data['Date'], '%d.%m.%Y').date()
            else:
                convert_date = data['Date']  # Already a date object
                
            logger.info(f"Using date: {convert_date} (type: {type(convert_date)})")

            try:
                mileage = int(data['mileage'])
            except (ValueError, TypeError) as e:
                logger.error(f"Error converting mileage to int: {e}")
                raise ValueError("Mileage must be a number")
            
            # Check if a record with this date already exists
            existing = await session.scalar(
                select(TO)
                .where(TO.date == convert_date)
            )
            if data['mark'] == 'mark_no':
                markup = find_markup_words(data['description'])
            else:
                markup = True
            if existing:
                # Update existing record
                existing.mileage = mileage
                existing.description = str(data['description'])
                await session.merge(existing)
                logger.info(f"Updated existing maintenance record for date: {convert_date}")
            else:
                # Create new record
                maintenance = TO(
                    date=convert_date,
                    mileage=mileage,
                    description=str(data['description']),
                    mark=markup
                )
                session.add(maintenance)
                logger.info("Created new maintenance record")
                
            await session.commit()
            return True
            
    except Exception as e:
        logger.error(f"Error in reg_maintance: {str(e)}", exc_info=True)
        if 'session' in locals():
            await session.rollback()
        return False



async def get_all_maintance(latest: bool = False):
    async with async_session() as session:
        result = await session.scalars(
            select(TO).
            order_by(TO.date.asc())
        )
        return result.all()

async def get_last_maintance():
    async with async_session() as session:
        return await session.scalar(
            select(TO).
            where(TO.mark == True).
            order_by(TO.date.desc()).
            limit(1)
        )



async def reg_consumption(data):
    try:
        consumption = Consumption(
            date=data['Date'],
            liters=Decimal(str(data['liters'])),
            mileage=data['mileage'],
            mean=Decimal(str(data['avg']))
        )
        async with async_session() as session:
            existing = await session.scalar(
                select(Consumption)
                .where(Consumption.date == data['Date'])
            )
            if existing:
                existing.liters = Decimal(str(data['liters']))
                existing.mileage = data['mileage']
                existing.mean = Decimal(str(data['avg']))
                await session.merge(existing)
                return True
            else:
                session.add(consumption)
            await session.commit()
            return True
    except Exception as e:
        if 'session' in locals():
            await session.rollback()
        return False

async def get_last_consumption():
    async with async_session() as session:
        return await session.scalar(
            select(Consumption).
            order_by(Consumption.date.desc()).
            limit(1)
        )

async def get_all_consumption():
    async with async_session() as session:
        result = await session.scalars(
            select(Consumption).
            order_by(Consumption.date.asc())
        )
        return result.all()
