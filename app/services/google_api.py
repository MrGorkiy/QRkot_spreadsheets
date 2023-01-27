from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_ROWCOUNT_DRAFT = 100
SPREADSHEET_COLUMNCOUNT_DRAFT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет на ',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=SPREADSHEET_ROWCOUNT_DRAFT,
            columnCount=SPREADSHEET_COLUMNCOUNT_DRAFT
        )
    ))]
)
TABLE_VALUES_DRAFT = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
ROW_COLUMN_COUNT_TOO_BIG = ('В ваших данных строк - {rows_value}, а'
                            'столбцов - {columns_value}, но'
                            'количество строк не'
                            'должно превышать {rowcount_draft}, '
                            'a столбцов - {columncount_draft}')


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаём документ."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheets_body = SPREADSHEET_BODY.copy()
    spreadsheets_body['properties']['title'] += now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляем права доступа."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_project: list[CharityProject],
        wrapper_services: Aiogoogle
) -> str:
    """Наполняем документ данными."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = TABLE_VALUES_DRAFT.copy()
    table_values[0].append(now_date_time)
    table_values = [*table_values,
                    *[list(map(str,
                               [project.name,
                                project.close_date - project.create_date,
                                project.description])) for project in
                      charity_project]
                    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    columns_value = max(len(items_to_count)
                        for items_to_count in table_values)
    rows_value = len(table_values)
    if (SPREADSHEET_ROWCOUNT_DRAFT < rows_value or
            SPREADSHEET_COLUMNCOUNT_DRAFT < columns_value):
        raise ValueError(ROW_COLUMN_COUNT_TOO_BIG.format(
            rows_value=rows_value,
            columns_value=columns_value,
            rowcount_draft=SPREADSHEET_ROWCOUNT_DRAFT,
            columncount_draft=SPREADSHEET_COLUMNCOUNT_DRAFT))

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_value}C{columns_value}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
    return spreadsheet_id
