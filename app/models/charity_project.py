from sqlalchemy import Column, String, Text

from .abstracts import InvestInfoAndDatesAbstractModel


class CharityProject(InvestInfoAndDatesAbstractModel):
    """Модель благотворительного проекта.

    Наследует базовые поля инвестирования из InvestInfoAndDatesAbstractModel:
    - full_amount: Требуемая сумма (должна быть > 0);
    - invested_amount: Собранная сумма;
    - fully_invested: Флаг завершения сбора;
    - create_date/close_date: Даты открытия/закрытия проекта.

    Собственные поля:
        name (str): Название проекта (макс. 100 символов, уникальное);
        description (str): Описание проекта (текст).
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return (f'{self.name}: собрано {self.invested_amount} '
                f'из {self.full_amount}')
