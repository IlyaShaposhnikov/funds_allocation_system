from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class InvestInfoAndDatesAbstractModel(Base):
    """Абстрактная модель для инвестиционных объектов с базовой структурой.

    Содержит общие поля и ограничения для объектов, связанных с инвестициями:
    - Благотворительные проекты (CharityProject)
    - Пожертвования (Donation)

    Атрибуты:
        full_amount (int): Требуемая/полная сумма. Должна быть > 0.
        invested_amount (int): Внесённая сумма. По умолчанию 0.
        fully_invested (bool): Флаг завершённости инвестирования.
        create_date (datetime): Дата создания записи (устанавливается
        автоматически).
        close_date (datetime): Дата завершения инвестирования (если применимо).

    Ограничения (CheckConstraint):
        1. full_amount > 0
        2. invested_amount >= 0
        3. invested_amount <= full_amount
    """
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_check'),
        CheckConstraint('invested_amount >= 0', name='invested_amount_check'),
        CheckConstraint('full_amount >= invested_amount',
                        name='amounts_check'),
    )

    full_amount = Column(Integer, nullable=False, default=0)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, nullable=True)
