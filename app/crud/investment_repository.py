from sqlalchemy.ext.asyncio import AsyncSession
from app.models import InvestInfoAndDatesAbstractModel
from app.services.investment_service import InvestmentService


class CRUDInvestment:
    """Работа с сессией БД для инвестиционных операций"""

    @staticmethod
    async def execute_distribution(
        source: InvestInfoAndDatesAbstractModel,
        targets: list[InvestInfoAndDatesAbstractModel],
        session: AsyncSession
    ) -> InvestInfoAndDatesAbstractModel:
        """Выполняет распределение средств с сохранением в БД"""
        result = await InvestmentService.distribute_funds(
            source, targets, session
        )

        for item in [result] + targets:
            session.add(item)
        await session.commit()
        await session.refresh(result)

        return result
