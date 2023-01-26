from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'comment': 'Все нашим любимым кошечкам!',
                'full_amount': 25
            }
        }


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
