from http import HTTPStatus
from typing import Generic, Optional, TypeVar

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Базовый репозиторий для CRUD операций с моделями SQLAlchemy.

    Предоставляет общие методы для работы с базой данных:
    - Создание (create);
    - Чтение (get, get_or_404, get_all);
    - Обновление (update);
    - Удаление (delete).
    """

    def __init__(self, model):
        self.model = model

    async def save(
        self,
        db_object: T,
        session: AsyncSession,
    ) -> T:
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def create(
            self,
            object_in,
            session: AsyncSession,
            user: Optional[T] = None
    ) -> T:
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = await self.save(self.model(**object_in_data), session)
        return db_object

    async def get(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> Optional[T]:
        objects = await session.execute(
            select(self.model).where(self.model.id == object_id))
        return objects.scalars().first()

    async def get_or_404(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> T:
        db_obj = await self.get(object_id, session)
        if db_obj is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'{self.model.__name__} с id {object_id} не найден'
            )
        return db_obj

    async def get_all(
            self,
            session: AsyncSession
    ) -> list[T]:
        objects = await session.execute(select(self.model))
        return objects.scalars().all()

    async def update(
            self,
            db_object: T,
            object_in,
            session: AsyncSession,
    ) -> T:
        if db_object is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Объект {self.model.__name__} не найден'
            )
        object_data = jsonable_encoder(db_object)
        if isinstance(object_in, dict):
            update_data = object_in
        else:
            update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        return await self.save(db_object, session)

    async def delete(
            self,
            db_object: T,
            session: AsyncSession,
    ) -> T:
        if db_object is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Объект {self.model.__name__} не найден'
            )
        await session.delete(db_object)
        await session.commit()
        return db_object
