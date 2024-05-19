from sqlalchemy import BigInteger, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    #id: int = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class TO(Base):
    __tablename__ = 'tos'
    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    mileage: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String)

class Exp(Base):
    __tablename__ = 'expends'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(Date)
    mileage: Mapped[int] = mapped_column()
    liters: Mapped[float] = mapped_column()
    mean: Mapped[float] = mapped_column()

async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
