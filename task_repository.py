from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Task


class TaskRepository:

    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def create(
        self,
        task: Task
    ):
        self.session.add(task)

        await self.session.commit()

        await self.session.refresh(task)

        return task

    async def get_by_id(
        self,
        task_id: int
    ):
        query = select(Task).where(
            Task.id == task_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_all(self):
        query = select(Task)

        result = await self.session.execute(query)

        return result.scalars().all()