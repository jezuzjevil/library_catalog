import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class Book(Base):
    """ORM-модель книги в каталоге."""

    __tablename__ = "books"

    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)

    author: Mapped[str] = mapped_column(String(300), nullable=False, index=True)

    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    genre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    pages: Mapped[int] = mapped_column(Integer, nullable=False)

    available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )

    # опциональные поля
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Временные метки
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    def __repr__(self) -> str:
        return f"<Book(id={self.book_id}, title='{self.title}')>"
