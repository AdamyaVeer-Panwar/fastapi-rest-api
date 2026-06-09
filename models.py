from datetime import datetime

from database import Base

from sqlalchemy import (
    Integer,
    String,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )