from models import Task
from task_repository import TaskRepository
from user_repository import UserRepository
from fastapi import HTTPException
from project_repository import ProjectRepository


class TaskService:

    def __init__(
        self,
        repository: TaskRepository,
        user_repository: UserRepository,
        project_repository: ProjectRepository
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.project_repository = project_repository

    async def create_task(
        self,
        title: str,
        user_id: int,
        project_id: int
    ):
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
            status_code=404,
            detail="User not found"
        )

        project = await self.project_repository.get_by_id(
        project_id
        )

        if not project:
            raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

        task = Task(
            title=title,
            user_id=user_id,
            project_id=project_id
        )

        return await self.repository.create(task)

    async def get_task(
        self,
        task_id: int
    ):
        return await self.repository.get_by_id(task_id)

    async def get_tasks(self):
        return await self.repository.get_all()
    
    