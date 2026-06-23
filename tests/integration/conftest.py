import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from models import Base


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:your_password@localhost:5432/test_db"
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False
    )

    # Create tables before tests start
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )

    yield engine

    # Remove tables after all tests finish
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.drop_all
        )

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):

    SessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()