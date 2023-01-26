from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.crud import charity_project_crud
from app.models import CharityProject

PROJECT_NOT_FOUND_ERROR = ('Проект не найден!')
PROJECT_EXISTS_ERROR = ('Проект с таким именем уже существует!')
FORBIDDEN_UPDATE_ERROR = ('Закрытый проект нельзя редактировать!')
INVESTED_RPOJECT_DELETION_ERROR = ('В проект были внесены средства, не '
                                   'подлежит удалению!')
INVALID_INVESTED_AMOUNT_ERROR = ('Сумма проекта не может быть меньше '
                                 'внесённой!')


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка на существование благотворительного проекта по id."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NOT_FOUND_ERROR
        )
    return charity_project


async def check_charity_project_name_unique(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    """Проверка на уникальность имени благотворительного проекта."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_EXISTS_ERROR
        )


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка на наличие инвестированных средств."""
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INVESTED_RPOJECT_DELETION_ERROR
        )
    return charity_project


async def check_charity_project_closed(project: CharityProject) -> None:
    """Проверит, закрыт ли проект."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FORBIDDEN_UPDATE_ERROR,
        )


async def check_correct_full_amount_for_update(
        project_id: int,
        session: AsyncSession,
        full_amount_to_update: int
):
    """Проверят возможность для редактирования проекта"""
    charity_project = await check_charity_project_exists(
        charity_project_id=project_id, session=session
    )
    if charity_project.invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=INVALID_INVESTED_AMOUNT_ERROR
        )


async def check_google_api_variables_are_set(settings: Settings):
    """Проверяет, что настроечные параметры Google API установлены."""
    if not all([settings.type,
                settings.project_id,
                settings.private_key_id,
                settings.private_key,
                settings.client_email,
                settings.client_id,
                settings.auth_uri,
                settings.token_uri,
                settings.auth_provider_x509_cert_url,
                settings.client_x509_cert_url,
                settings.email]):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=('Невозможно сформировать отчет. '
                    'Ошибка в конфигурационных параметрах. '
                    'Проверьте настройки Google API.')
        )
