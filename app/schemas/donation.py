from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема для пожертвования с необязательными полями."""

    comment: Optional[str]
    full_amount: Optional[PositiveInt]


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""

    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationForUserDB(DonationCreate):
    """Схема для возврата пожертвования пользователю (без служебных полей)."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationForAdminDB(DonationForUserDB):
    """Схема для возврата пожертвования администратору (со всеми полями)."""

    user_id: int
    invested_amount: int
    fully_invested: bool = False
    close_date: Optional[datetime]
