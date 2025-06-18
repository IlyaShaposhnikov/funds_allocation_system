from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel
from app.services.investment_service import InvestmentService


async def distribute_donations(
    distributed: InvestInfoAndDatesAbstractModel,
    destinations: list[InvestInfoAndDatesAbstractModel],
    session: AsyncSession
) -> InvestInfoAndDatesAbstractModel:
    """Распределяет пожертвования по незавершенным проектам.

    Note:
        Автоматически сохраняет все изменения в базе данных.
        Использует алгоритм "первый пришел - первый обслужен" (FIFO).
    """
    return await InvestmentService.distribute_funds(
        distributed, destinations, session
    )
