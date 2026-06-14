from models import User
from user_repository import UserRepository
import json

from redis_client import redis_client

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
        cache_key = f"user:{user_id}"

        cached_user = await redis_client.get(
            cache_key
        )

        if cached_user:
            print("CACHE HIT")

            return json.loads(
                cached_user
            )

        print("CACHE MISS")

        user = await self.repository.get_by_id(
            user_id
        )

        if not user:
            return None

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

        await redis_client.set(
            cache_key,
            json.dumps(user_data),
            ex=300
        )

        return user_data

    async def get_users(self):
        return await self.repository.get_all()