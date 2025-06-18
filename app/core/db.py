from http import HTTPStatus
from collections.abc import AsyncGenerator

from fastapi.exceptions import HTTPException
from sqlalchemy import Column, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Ошибка при выполнении операции.'
            )
