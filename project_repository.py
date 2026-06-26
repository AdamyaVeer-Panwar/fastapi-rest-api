from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project: Project):
        self.session.add(project)

        await self.session.commit()

        await self.session.refresh(project)

        return project

    async def get_by_id(self, project_id: int):
        query = select(Project).where(Project.id == project_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_all(self):
        query = select(Project)

        result = await self.session.execute(query)

        return result.scalars().all()
