from models import Task
from task_repository import TaskRepository


class TaskService:

    def __init__(
        self,
        repository: TaskRepository
    ):
        self.repository = repository

    async def create_task(
        self,
        title: str,
        user_id: int,
        project_id: int
    ):
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