from decimal import Decimal

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)


class TO(Base):
    __tablename__ = "maintance"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    mileage: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String)
    mark: Mapped[bool] = mapped_column()
class Consumption(Base):
    __tablename__ = "consumption"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    mileage: Mapped[int] = mapped_column()
    liters: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    mean: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
