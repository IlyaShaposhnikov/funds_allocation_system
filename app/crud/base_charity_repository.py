from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_repository import BaseRepository
from app.models import CharityProject, Donation
from app.services.close_service import CloseService

T = TypeVar('T', CharityProject, Donation)


class BaseCharityRepository(BaseRepository[T]):
    """Базовый репозиторий для работы с благотворительными объектами.

    Обеспечивает общие операции для моделей CharityProject и Donation.
    """

    def __init__(self, model):
        super().__init__(model)

    async def get_opens(
            self,
            session: AsyncSession
    ) -> list[T]:
        """Получает список всех открытых (незавершенных) объектов.

        Возвращает объекты, отсортированные по дате создания (от старых
        к новым).
        """
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()

    async def close(
            self,
            db_object: T,
            session: AsyncSession
    ) -> T:
        """Закрывает объект (помечает как fully_invested).

        Использует сервис CloseService для выполнения операции закрытия.
        """
        return await CloseService.close_investment(db_object, session)
