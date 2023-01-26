from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_name_unique,
                                check_correct_full_amount_for_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.donation_functions import allocate_donation_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Просмотр списка всех благотворительных проектов.'
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Условия:
    - Доступно для всех посетителей.
    """
    return await charity_project_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создает благотворительный проект.'
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Условия:
    - Только для суперпользователей.
    """
    await check_charity_project_name_unique(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    await allocate_donation_funds(new_charity_project, session=session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет благотворительный проект.'
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Условия:
    - Только для суперпользователей.
    - Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    charity_project = await check_charity_project_before_delete(
        charity_project_id=project_id, session=session
    )
    deleted_charity_project = await charity_project_crud.delete(
        db_obj=charity_project, session=session
    )
    return deleted_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Редактирует благотворительный проект.'
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Условия:
    - Только для суперпользователей.
    - Закрытый проект нельзя редактировать.
    - Нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_closed(charity_project)

    if object_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, object_in.full_amount
        )

    if object_in.name is not None:
        await check_charity_project_name_unique(
            object_in.name, session
        )

    charity_project = await charity_project_crud.update(
        charity_project, object_in, session
    )
    await allocate_donation_funds(charity_project, session=session)
    return charity_project
