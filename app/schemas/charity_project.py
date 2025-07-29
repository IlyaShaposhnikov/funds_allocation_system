from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовая схема для проекта с необязательными полями."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового благотворительного проекта."""

    name: str = Field(
        ..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления существующего проекта с валидацией полей."""

    @validator('name')
    def name_cannot_be_empty(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема для возврата проекта из БД со всеми служебными полями."""

    id: int
    invested_amount: int
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
