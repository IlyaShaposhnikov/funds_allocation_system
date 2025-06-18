from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_charity_repository import BaseCharityRepository
from app.models import CharityProject


class CRUDCharityProject(BaseCharityRepository[CharityProject]):
    """CRUD-репозиторий для работы с благотворительными проектами.

    Наследует базовые CRUD-операции от BaseCharityRepository и добавляет
    специфичные методы для работы с проектами.
    """

    @staticmethod
    async def get_id_by_name(
            name: str,
            session: AsyncSession
    ) -> Optional[int]:
        project = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name))
        return project.scalars().first()

    async def close(
            self,
            db_object: CharityProject,
            session: AsyncSession
    ) -> CharityProject:
        db_object.fully_invested = True
        db_object.close_date = datetime.utcnow()
        return await self.save(db_object, session)

    async def get_or_404(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> CharityProject:
        project = await self.get(object_id, session)
        if project is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Проект с id {object_id} не найден'
            )
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
