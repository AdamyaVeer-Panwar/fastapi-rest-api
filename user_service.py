from models import User
from user_repository import UserRepository


class UserService:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def create_user(
        self,
        name: str,
        email: str
    ):
        user = User(
            name=name,
            email=email
        )

        return await self.repository.create(user)

    async def get_user(
        self,
        user_id: int
    ):
        return await self.repository.get_by_id(user_id)

    async def get_users(self):
        return await self.repository.get_all()