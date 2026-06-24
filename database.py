from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

from config import DATABASE_URL


# ----------------------------
# ORM Base
# ----------------------------
class Base(DeclarativeBase):
    pass


# ----------------------------
# Engine factory (IMPORTANT FIX)
# ----------------------------
def create_engine(database_url: str):
    """
    Creates a new SQLAlchemy async engine.
    This prevents import-time binding issues and enables testing overrides.
    """
    return create_async_engine(
        database_url,
        echo=False,

        # IMPORTANT:
        # In tests, connection pooling often causes hidden state leakage.
        # NullPool ensures each connection is fresh and isolated.
        poolclass=NullPool,
    )


# ----------------------------
# Session factory
# ----------------------------
def create_sessionmaker(engine):
    """
    Creates session factory bound to a specific engine.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# ----------------------------
# Default (production) setup
# ----------------------------
engine = create_engine(DATABASE_URL)
AsyncSessionLocal = create_sessionmaker(engine)


# ----------------------------
# Dependency (FastAPI)
# ----------------------------
async def get_db():
    """
    FastAPI dependency.
    Always yields a fresh session per request.
    """
    async with AsyncSessionLocal() as session:
        yield session