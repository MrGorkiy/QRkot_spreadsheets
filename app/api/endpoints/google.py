from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_google_api_variables_are_set
from app.core.config import settings
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()

GOOGLE_SHEETS_URL = 'https://docs.google.com/spreadsheets/d/'


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    summary='Отчет по закрытым проектам'
)
async def get_spreadsheet_report(
        aiogoogle_object: Aiogoogle = Depends(get_service),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Формирует отчет по закрытым благотворительным проектам.
    """
    await check_google_api_variables_are_set(settings=settings)
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(aiogoogle_object)
    await set_user_permissions(spreadsheet_id, aiogoogle_object)
    await spreadsheets_update_value(spreadsheet_id, projects, aiogoogle_object)
    return GOOGLE_SHEETS_URL + spreadsheet_id
