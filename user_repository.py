from sqlalchemy.ext.asyncio import AsyncSession

from models import User

from sqlalchemy import select


class UserRepository:

    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def get_by_id(
        self,
        user_id: int
    ) -> User | None:
        query = select(User).where(
            User.id == user_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()