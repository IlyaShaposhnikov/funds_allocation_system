from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstracts import InvestInfoAndDatesAbstractModel


class Donation(InvestInfoAndDatesAbstractModel):
    """Модель пожертвования в благотворительный проект.

    Наследует базовые поля из InvestInfoAndDatesAbstractModel:
    - full_amount: Сумма пожертвования (должна быть > 0);
    - invested_amount: Часть суммы, распределённая по проектам;
    - fully_invested: Флаг полного распределения средств;
    - create_date/close_date: Даты создания/распределения.

    Собственные поля:
        user_id (int): ID пользователя, сделавшего пожертвование
                       (внешний ключ к таблице user);
        comment (str, optional): Комментарий к пожертвованию.
    """

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
