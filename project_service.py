from models import Project
from project_repository import ProjectRepository


class ProjectService:

    def __init__(
        self,
        repository: ProjectRepository
    ):
        self.repository = repository

    async def create_project(
        self,
        name: str,
        user_id: int
    ):
        project = Project(
            name=name,
            user_id=user_id
        )

        return await self.repository.create(project)

    async def get_project(
        self,
        project_id: int
    ):
        return await self.repository.get_by_id(project_id)

    async def get_projects(self):
        return await self.repository.get_all()