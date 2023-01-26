from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Базовая настройка таблиц БД."""

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Асинхронный генератор сессий.

    Через асинхронный контекстный менеджер и sessionmaker открывается сессия.
    Генератор с сессией передается в вызывающую функцию.
    Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
    и при выходе из контекстного менеджера сессия будет закрыта.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
