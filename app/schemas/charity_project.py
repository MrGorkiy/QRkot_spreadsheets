from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовая схема.
    :param str name: Название проекта.
    :param str description: Описание проекта.
    :param int full_amount: Цель сбора средств.
    """
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    """Схема для полученных данных."""
    name: str = Field(..., max_length=100)
    description: str = Field(..., )
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'name': 'Бездомные котики',
                'description': 'Средства идут на постройку приюта для котиков',
                'full_amount': 1200
            }
        }


class CharityProjectDB(CharityProjectCreate):
    """Схема для возвращаемого объекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Схема для полученных данных."""
    name: Optional[str] = Field(max_length=100, )
    description: Optional[str] = Field()
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Голодающие котики',
                'description': 'Закупка питания для котиков',
                'full_amount': 500
            }
        }
