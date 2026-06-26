import asyncio

from models import User
from database import AsyncSessionLocal


async def main():
    async with AsyncSessionLocal() as session:
        user = User(email="adamya@example.com", name="Adamya")

        session.add(user)

        await session.commit()

        print("User created")


if __name__ == "__main__":
    asyncio.run(main())
