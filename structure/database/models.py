from dotenv import load_dotenv
from sqlalchemy import BigInteger, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import os
load_dotenv()

DB_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///db.sqlite3')

# Lazy engine/session creation to avoid import-time driver errors during Alembic runs
engine = None
async_session = None
try:
    engine = create_async_engine(DB_URL, pool_pre_ping=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
except ModuleNotFoundError:
    # Alembic or environment without async driver: engine will be None
    engine = None
    async_session = None


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    #id: int = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class TO(Base):
    __tablename__ = 'maintance'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    mileage: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String)
    mark: Mapped[bool] = mapped_column()

class Exp(Base):
    __tablename__ = 'expends'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(Date)
    mileage: Mapped[int] = mapped_column()
    liters: Mapped[float] = mapped_column()
    mean: Mapped[float] = mapped_column()

async def db_main():
    if engine is None:
        # Running in an environment without async driver (e.g., Alembic context)
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
