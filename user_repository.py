from sqlalchemy.ext.asyncio import AsyncSession

from models import User

from sqlalchemy import select


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def create(self, user: User):
        self.session.add(user)

        await self.session.commit()

        await self.session.refresh(user)

        return user

    async def get_all(self):
        query = select(User)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def update(self, user_id: int, name: str, email: str):
        user = await self.get_by_id(user_id)

        if not user:
            return None

        user.name = name
        user.email = email

        await self.session.commit()

        await self.session.refresh(user)

        return user
