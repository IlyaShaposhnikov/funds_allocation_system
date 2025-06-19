from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel
from app.crud.base_repository import BaseRepository  # noqa


class InvestmentService:
    """Сервис для работы с инвестиционными операциями.

    Предоставляет методы для:
    - Расчета остатка средств
    - Пометки объектов как полностью проинвестированных
    - Распределения средств между объектами
    """

    @staticmethod
    def get_remaining_amount(
        invested_object: InvestInfoAndDatesAbstractModel
    ) -> int:
        """Вычисляет остаток средств для инвестирования/распределения.
        """
        return invested_object.full_amount - invested_object.invested_amount

    @staticmethod
    def mark_as_fully_invested(
        invested_object: InvestInfoAndDatesAbstractModel
    ) -> None:
        """Помечает объект как полностью проинвестированный.

        Устанавливает:
        - invested_amount = full_amount
        - fully_invested = True
        - close_date = текущая дата/время
        """
        invested_object.invested_amount = invested_object.full_amount
        invested_object.fully_invested = True
        invested_object.close_date = datetime.now()

    @staticmethod
    async def distribute_funds(
        distributed: InvestInfoAndDatesAbstractModel,
        destinations: list[InvestInfoAndDatesAbstractModel],
        session: AsyncSession
    ) -> InvestInfoAndDatesAbstractModel:
        """Распределяет средства между объектами по алгоритму FIFO.

        Алгоритм:
        1. Итерирует по получателям в порядке очереди
        2. Распределяет средства пока не закончатся:
           - Либо средства источника
           - Либо потребности получателей
        3. Помечает полностью заполненные объекты
        4. Сохраняет все изменения в БД
        """
        processed_items = [distributed]
        for destination in destinations:
            processed_items.append(destination)
            distributed_remainder = (InvestmentService.
                                     get_remaining_amount(distributed))
            destination_remainder = (InvestmentService.
                                     get_remaining_amount(destination))
            if distributed_remainder <= destination_remainder:
                destination.invested_amount += distributed_remainder
                distributed.invested_amount = distributed.full_amount
                if destination.invested_amount >= destination.full_amount:
                    destination.fully_invested = True
                    destination.close_date = datetime.now()
                if distributed.invested_amount >= distributed.full_amount:
                    distributed.fully_invested = True
                    distributed.close_date = datetime.now()
                break
            else:
                destination.invested_amount = destination.full_amount
                destination.fully_invested = True
                destination.close_date = datetime.now()
                distributed.invested_amount += destination.full_amount
                if distributed.invested_amount >= distributed.full_amount:
                    distributed.fully_invested = True
                    distributed.close_date = datetime.now()
                    break

        return distributed
