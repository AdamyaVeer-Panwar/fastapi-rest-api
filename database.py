from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    pass

DATABASE_URL = (
    "postgresql+asyncpg://postgres:your_password@localhost:5432/task_manager"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    db = AsyncSessionLocal()

    try:
        yield db

    finally:
        await db.close()
        