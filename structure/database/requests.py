import datetime

from structure.database.models import async_session
from structure.database.models import User, TO, Exp
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
            if data['Mark'] == 'mark_no':
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
        if latest:
            return await session.scalar(select(TO).order_by(TO.date.desc()).limit(1))
        else:
            result = await session.scalars(select(TO).order_by(TO.date.asc()))
            return result.all()