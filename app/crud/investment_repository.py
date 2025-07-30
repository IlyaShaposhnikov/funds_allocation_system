from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel


class CRUDInvestment:
    """Работа с сессией БД для инвестиционных операций."""

    @staticmethod
    async def save_investment_objects(
        session: AsyncSession,
        *objects: InvestInfoAndDatesAbstractModel
    ) -> None:
        """Сохраняет инвестиционные объекты в БД."""
        for obj in objects:
            session.add(obj)
        await session.commit()
        for obj in objects:
            await session.refresh(obj)
