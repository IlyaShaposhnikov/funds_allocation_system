from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_charity_repository import BaseCharityRepository
from app.models import Donation, User


class CRUDDonation(BaseCharityRepository[Donation]):
    """CRUD-репозиторий для работы с пожертвованиями.

    Наследует базовые CRUD-операции от BaseCharityRepository и добавляет
    специфичные методы для работы с пожертвованиями.
    """

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[List[Donation]]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
