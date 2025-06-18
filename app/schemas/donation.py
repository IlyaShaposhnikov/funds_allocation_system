from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[PositiveInt]


class DonationCreate(DonationBase):
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationForUserDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationForAdminDB(DonationForUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool = False
    close_date: Optional[datetime]
