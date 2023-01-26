from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB
from app.services.donation_functions import allocate_donation_funds

EXCLUDE_FIELDS = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Просмотр списка всех пожертвований.'
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Условия:
    - Доступно только для суперпользователей.
    """
    return await donation_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={*EXCLUDE_FIELDS},
    summary='Создать пожертвование.'
)
async def create_donation(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Условия:
    - Доступно для авторизированного пользователя.
    """
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await allocate_donation_funds(new_donation, session=session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={*EXCLUDE_FIELDS},
    summary='Посмотреть список пожертвований текущего пользователя.'
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Условия:
    - Доступно для авторизированного пользователя.
    """
    return await donation_crud.get_user_donations(user=user, session=session)
