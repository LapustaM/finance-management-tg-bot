from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, select, func, extract, delete
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_async_engine(DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String)
    date: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[str] = mapped_column(String)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_expense(amount: int, category: str, user_id: str, date=None):
    if date is None:
        date = datetime.now()
    async with new_session() as session:
        expense = Expense(
            amount=amount,
            category=category,
            date=date,
            user_id=user_id
        )
        session.add(expense)
        await session.commit()

async def remove_all_expenses(user_id: str):
    async with new_session() as session:
        query = delete(Expense).where(Expense.user_id == user_id)
        await session.execute(query)
        await session.commit()

async def get_stats(user_id: str, period: str = "all"):
    async with new_session() as session:
        query = select(func.sum(Expense.amount)).where(Expense.user_id == user_id)

        match period:
            case "month":
                query = query.filter(extract('month', Expense.date) == datetime.now().month, extract('year', Expense.date) == datetime.now().year)
            case "year":
                query = query.filter(extract('year', Expense.date) == datetime.now().year)
            case "all":
                pass
            case _:
                raise ValueError("Invalid period, use 'month', 'year' or 'all'")

        result = await session.execute(query)
        total = result.scalar()
        return total if total else 0