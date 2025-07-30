from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel


class CloseService:
    """Сервис для закрытия инвестиционных объектов (проектов/пожертвований).

    Предоставляет статический метод для пометки объекта как полностью
    проинвестированного с установкой даты закрытия и сохранением
    изменений в БД.
    """

    @staticmethod
    async def close_investment(
        investment: InvestInfoAndDatesAbstractModel,
        session: AsyncSession
    ) -> InvestInfoAndDatesAbstractModel:
        """Помечает инвестиционный объект как закрытый (fully_invested).
        Устанавливает флаг fully_invested в True и текущую дату в close_date,
        затем сохраняет изменения в базе данных.
        """
        investment.fully_invested = True
        investment.close_date = datetime.utcnow()
        await session.commit()
        await session.refresh(investment)
        return investment
