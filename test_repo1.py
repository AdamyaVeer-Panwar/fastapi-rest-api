# test_repository.py

import asyncio

from database import AsyncSessionLocal
from user_repository import UserRepository


async def main():
    async with AsyncSessionLocal() as session:

        repository = UserRepository(session)

        user = await repository.get_by_id(1)

        print(user.id)
        print(user.name)
        print(user.email)


if __name__ == "__main__":
    asyncio.run(main())