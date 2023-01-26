from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        charity_project = await session.execute(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        return charity_project.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        return sorted(
            projects.scalars().all(),
            key=lambda obj: obj.close_date - obj.create_date
        )


charity_project_crud = CRUDCharityProject(CharityProject)
